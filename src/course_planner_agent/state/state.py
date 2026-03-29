from typing import TypedDict, List, Optional, Dict, Any
from langchain_core.documents import Document


class GraphState(TypedDict, total=False):
    """
    Shared state across LangGraph nodes
    """

    # User input
    query: str

    # Parsed student profile (from intake)
    student_profile: Optional[Dict[str, Any]]

    # Retrieved documents
    retrieved_docs: Optional[List[Document]]

    # Generated answer/plan
    answer: Optional[str]

    # Citations extracted
    citations: Optional[List[str]]

    # Clarifying questions (if needed)
    clarifying_questions: Optional[List[str]]

    # Final validated output
    final_output: Optional[str]

    # Errors / flags
    error: Optional[str]