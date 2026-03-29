from groq import Groq
import os

from src.course_planner_agent.state.state import GraphState
from src.course_planner_agent.utils.logger import logger
from src.course_planner_agent.utils.prompt_loader import load_prompt


VERIFIER_PROMPT_PATH = "src/course_planner_agent/prompts/verifier_prompt.txt"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def verifier_node(state: GraphState) -> GraphState:
    """
    LLM-based verification:
    - checks citations
    - removes hallucinations
    - enforces abstention
    """
    try:
        logger.info("Running Verifier Node")

        answer = state.get("answer", "")

        if not answer:
            state["error"] = "No answer generated"
            return state

        #  Load verifier prompt
        verifier_prompt = load_prompt(VERIFIER_PROMPT_PATH)

        #  Create verification input
        verification_input = f"""
Response to verify:

{answer}
"""

        #  LLM verification
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": verifier_prompt},
                {"role": "user", "content": verification_input}
            ],
            temperature=0
        )

        final_output = response.choices[0].message.content

        # Optional: extract citations again (simple regex)
        import re
        citations = list(set(re.findall(r"\[Chunk\s*\d+\]", final_output)))

        state["citations"] = citations
        state["final_output"] = final_output

        logger.info(f"Verifier completed with {len(citations)} citations")

        return state

    except Exception as e:
        logger.error(f"Verifier Node failed: {e}")
        state["error"] = str(e)
        return state