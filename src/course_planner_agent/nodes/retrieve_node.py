from src.course_planner_agent.state.state import GraphState
from src.course_planner_agent.vectorstore.faiss_store import load_faiss_index
from src.course_planner_agent.vectorstore.retriever import get_retriever, retrieve_documents
from src.course_planner_agent.utils.logger import logger


FAISS_INDEX_PATH = "vector_db/faiss_index"


def retrieve_node(state: GraphState) -> GraphState:
    """
    Retrieves relevant documents using FAISS
    """
    try:
        logger.info("Running Retrieve Node")

        query = state.get("query", "")

        # Load vector store
        vectorstore = load_faiss_index(FAISS_INDEX_PATH)

        # Create retriever
        retriever = get_retriever(vectorstore, k=5)

        # Retrieve docs
        docs = retrieve_documents(retriever, query)

        state["retrieved_docs"] = docs

        logger.info("Documents retrieved successfully")

        return state

    except Exception as e:
        logger.error(f"Retrieve Node failed: {e}")
        state["error"] = str(e)
        return state