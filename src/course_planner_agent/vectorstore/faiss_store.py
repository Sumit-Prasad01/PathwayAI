from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from typing import List
from langchain_core.documents import Document
from src.course_planner_agent.utils.logger import logger


def build_faiss_index(documents: List[Document], save_path: str):
    try:
        logger.info("Building FAISS index...")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=embeddings
        )

        vectorstore.save_local(save_path)

        logger.info(f"FAISS index saved at {save_path}")

    except Exception as e:
        logger.error(f"Error building FAISS index: {e}")
        raise


def load_faiss_index(load_path: str) -> FAISS:
    try:
        logger.info(f"Loading FAISS index from {load_path}")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorstore = FAISS.load_local(
            load_path,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )

        return vectorstore

    except Exception as e:
        logger.error(f"Error loading FAISS index: {e}")
        raise