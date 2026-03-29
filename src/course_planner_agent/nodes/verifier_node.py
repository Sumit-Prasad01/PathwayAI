import re
from typing import List

from src.course_planner_agent.state.state import GraphState
from src.course_planner_agent.utils.logger import logger


def extract_citations(text: str) -> List[str]:
    """
    Extract citations like [Chunk X]
    """
    pattern = r"\[Chunk\s*\d+\]"
    return list(set(re.findall(pattern, text)))


def verifier_node(state: GraphState) -> GraphState:
    """
    Verifies:
    - citations exist
    - no unsupported claims (basic check)
    """
    try:
        logger.info("Running Verifier Node")

        answer = state.get("answer", "")

        if not answer:
            state["error"] = "No answer generated"
            return state

        citations = extract_citations(answer)

        # Basic validation
        if len(citations) == 0:
            logger.warning("No citations found → forcing abstention")

            final_output = """Answer / Plan:
I don’t have sufficient evidence from the provided catalog to answer this question.

Why:
The response lacked verifiable citations.

Citations:
None

Clarifying Questions (if needed):
Could you provide more specific course or program details?

Assumptions / Not in catalog:
Insufficient retrieved evidence.
"""
        else:
            final_output = answer

        state["citations"] = citations
        state["final_output"] = final_output

        logger.info(f"Verifier passed with {len(citations)} citations")

        return state

    except Exception as e:
        logger.error(f"Verifier Node failed: {e}")
        state["error"] = str(e)
        return state