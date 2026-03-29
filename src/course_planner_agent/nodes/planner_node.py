from langchain_groq import ChatGroq
import os
import json

from src.course_planner_agent.state.state import GraphState
from src.course_planner_agent.utils.logger import logger
from src.course_planner_agent.utils.prompt_loader import load_prompt

from dotenv import load_dotenv
load_dotenv()

SYSTEM_PROMPT_PATH = "src/course_planner_agent/prompts/system_prompt.txt"
PLANNER_PROMPT_PATH = "src/course_planner_agent/prompts/planner_prompt.txt"


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)


def format_docs(docs) -> str:
    formatted = []
    for doc in docs:
        content = doc.page_content
        chunk_id = doc.metadata.get("chunk_id", "N/A")
        formatted.append(f"[Chunk {chunk_id}]\n{content}")
    return "\n\n".join(formatted)


def safe_json_load(text: str):
    import json
    import re

    # Clean common issues
    text = text.strip()

    # Remove markdown if present
    text = text.replace("```json", "").replace("```", "")

    # Try direct parse
    try:
        return json.loads(text)
    except:
        pass

    # Extract JSON block
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    # FINAL FALLBACK (VERY IMPORTANT)
    return {
        "answer": text,
        "why": "Parsing failed",
        "citations": [],
        "clarifying_questions": [],
        "assumptions": "Model did not return valid JSON"
    }

def planner_node(state: GraphState) -> GraphState:
    try:
        logger.info("Running Planner Node")

        query = state.get("query", "")
        docs = state.get("retrieved_docs", [])

        context = format_docs(docs)

        system_prompt = load_prompt(SYSTEM_PROMPT_PATH)
        planner_template = load_prompt(PLANNER_PROMPT_PATH)

        prompt = planner_template.format(
            context=context,
            query=query
        )

        response = llm.invoke([
            ("system", system_prompt),
            ("human", prompt)
        ])

        raw_output = response.content

        logger.info(f"RAW LLM OUTPUT:\n{raw_output}")

        parsed = safe_json_load(raw_output)

        state["answer"] = parsed

        logger.info("Planner Node completed (LangChain Groq)")

        return state

    except Exception as e:
        logger.error(f"Planner Node failed: {e}")
        state["error"] = str(e)
        return state