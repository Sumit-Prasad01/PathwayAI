from typing import List
from groq import Groq
import os

from src.course_planner_agent.state.state import GraphState
from src.course_planner_agent.utils.logger import logger


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

        prompt = f"""
You are a Course Planning Assistant.

RULES:
- Use ONLY the provided context
- DO NOT guess
- If not found, say: "I don’t have that information in the provided catalog."
- EVERY claim must include citation (Chunk ID)

CONTEXT:
{context}

QUESTION:
{query}

OUTPUT FORMAT:

Answer / Plan:
Why:
Citations:
Clarifying Questions (if needed):
Assumptions / Not in catalog:
"""

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
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