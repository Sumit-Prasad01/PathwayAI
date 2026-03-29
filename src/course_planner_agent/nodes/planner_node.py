from groq import Groq
import os

from src.course_planner_agent.state.state import GraphState
from src.course_planner_agent.utils.logger import logger
from src.course_planner_agent.utils.prompt_loader import load_prompt


SYSTEM_PROMPT_PATH = "src/course_planner_agent/prompts/system_prompt.txt"
PLANNER_PROMPT_PATH = "src/course_planner_agent/prompts/planner_prompt.txt"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def format_docs(docs) -> str:
    """
    Convert retrieved docs into context string
    """
    formatted = []
    for doc in docs:
        content = doc.page_content
        meta = doc.metadata
        chunk_id = meta.get("chunk_id", "N/A")
        formatted.append(f"[Chunk {chunk_id}]\n{content}")

    return "\n\n".join(formatted)


def planner_node(state: GraphState) -> GraphState:
    """
    Generates answer / plan using Groq LLaMA 70B
    """
    try:
        logger.info("Running Planner Node")

        query = state.get("query", "")
        docs = state.get("retrieved_docs", [])

        context = format_docs(docs)

        # Load prompts
        system_prompt = load_prompt(SYSTEM_PROMPT_PATH)
        planner_template = load_prompt(PLANNER_PROMPT_PATH)

        #  Inject variables
        prompt = planner_template.format(
            context=context,
            query=query
        )

        # Proper LLM call with system + user roles
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        state["answer"] = answer

        logger.info("Planner Node completed")

        return state

    except Exception as e:
        logger.error(f"Planner Node failed: {e}")
        state["error"] = str(e)
        return state