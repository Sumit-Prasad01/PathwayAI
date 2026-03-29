import os
from dotenv import load_dotenv

from src.course_planner_agent.ingestion.pipeline import run_ingestion_pipeline
from src.course_planner_agent.vectorstore.faiss_store import build_faiss_index
from src.course_planner_agent.utils.logger import logger


load_dotenv()

DATA_PATH = "data/raw/dataset.pdf"
INDEX_PATH = "vector_db/faiss_index"


def main():
    try:
        logger.info("Starting index building process")

        # Step 1: Ingest + Chunk
        documents = run_ingestion_pipeline(DATA_PATH)

        # Step 2: Build FAISS index
        build_faiss_index(documents, INDEX_PATH)

        logger.info("Index building completed successfully")

    except Exception as e:
        logger.error(f"Index building failed: {e}")


if __name__ == "__main__":
    main()