from langchain_groq import ChatGroq
import os
import json
import re

from src.course_planner_agent.state.state import GraphState
from src.course_planner_agent.utils.logger import logger
from src.course_planner_agent.utils.prompt_loader import load_prompt
from src.course_planner_agent.schemas.response_schema import ResponseSchema

from dotenv import load_dotenv
load_dotenv()

VERIFIER_PROMPT_PATH = "src/course_planner_agent/prompts/verifier_prompt.txt"

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)


def verifier_node(state: GraphState) -> GraphState:
    try:
        logger.info("Running Verifier Node")

        answer = state.get("answer", {})

        if not answer:
            state["error"] = "No answer generated"
            return state

        verifier_prompt = load_prompt(VERIFIER_PROMPT_PATH)

        answer_text = json.dumps(answer, indent=2)

        verification_input = f"""
Response to verify:

{answer_text}
"""

        response = llm.invoke([
            ("system", verifier_prompt),
            ("human", verification_input)
        ])

        final_text = response.content
        final_text = re.split(r"The response is valid", final_text)[0].strip()

        citations = list(set(re.findall(r"\[Chunk\s*\d+\]", final_text)))

        response_obj = ResponseSchema(
            answer=final_text,
            citations=citations,
            clarifying_questions=[],
            assumptions=None,
            error=None
        )

        state["citations"] = citations
        state["final_output"] = response_obj.dict()

        logger.info(f"Verifier completed with {len(citations)} citations")

        return state

    except Exception as e:
        logger.error(f"Verifier Node failed: {e}")

        state["final_output"] = ResponseSchema(
            answer=None,
            citations=[],
            clarifying_questions=[],
            assumptions=None,
            error=str(e)
        ).dict()

        state["error"] = str(e)

        return state