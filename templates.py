import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "course_planner_agent"

list_of_files = [

    # ---------------- SOURCE ----------------
    f"src/{project_name}/__init__.py",

    # ---------------- INGESTION ----------------
    f"src/{project_name}/ingestion/loader.py",
    f"src/{project_name}/ingestion/chunker.py",
    f"src/{project_name}/ingestion/pipeline.py",

    # ---------------- VECTOR STORE ----------------
    f"src/{project_name}/vectorstore/faiss_store.py",
    f"src/{project_name}/vectorstore/retriever.py",

    # ---------------- LANGGRAPH CORE ----------------
    f"src/{project_name}/graph/builder.py",
    f"src/{project_name}/graph/workflow.py",

    # ---------------- NODES (AGENTS) ----------------
    f"src/{project_name}/nodes/intake_node.py",
    f"src/{project_name}/nodes/retrieve_node.py",
    f"src/{project_name}/nodes/planner_node.py",
    f"src/{project_name}/nodes/verifier_node.py",

    # ---------------- STATE ----------------
    f"src/{project_name}/state/state.py",

    # ---------------- PROMPTS ----------------
    f"src/{project_name}/prompts/system_prompt.txt",
    f"src/{project_name}/prompts/planner_prompt.txt",
    f"src/{project_name}/prompts/verifier_prompt.txt",

    # ---------------- SCHEMAS ----------------
    f"src/{project_name}/schemas/student_profile.py",
    f"src/{project_name}/schemas/response_schema.py",

    # ---------------- UTILS ----------------
    f"src/{project_name}/utils/logger.py",

    # ---------------- DATA ----------------
    "data/raw/dataset.pdf",
    "data/sources/sources.md",

    # ---------------- VECTOR DB ----------------
    "vector_db/faiss_index/.gitkeep",

    # ---------------- EVALUATION ----------------
    "evaluation/test_queries.json",
    "evaluation/evaluator.py",

    # ---------------- SCRIPTS ----------------
    "scripts/build_index.py",
    "scripts/run_graph.py",
    "scripts/run_evaluation.py",

    # ---------------- DEMO ----------------
    "demo/streamlit_app.py",

    # ---------------- ROOT ----------------
    ".env",
    "requirements.txt",
    "README.md"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir = filepath.parent

    if filedir != Path(""):
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir}")

    if not filepath.exists():
        filepath.touch()
        logging.info(f"Creating file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")