# 🎓 CoursePilot AI --- Agentic RAG Course Planning Assistant

An AI-powered system that helps students plan courses using academic
catalog data with **grounded reasoning, citations, and safe
abstention**.

------------------------------------------------------------------------

## 🚀 Features

-   📚 Multi-hop prerequisite reasoning\
-   🧠 Course eligibility validation\
-   📊 Course planning recommendations\
-   ❓ Clarifying questions for missing info\
-   🚫 Safe abstention (no hallucinations)\
-   🔍 Citation-backed responses

------------------------------------------------------------------------

## 🏗️ Architecture

User Query → Intake Node → Retriever (FAISS) → Planner (LLM) → Verifier
→ Final Output

------------------------------------------------------------------------

## ⚙️ Tech Stack

-   LangGraph (workflow orchestration)\
-   LangChain (RAG pipeline)\
-   FAISS (vector store)\
-   Sentence Transformers (embeddings)\
-   Groq (LLaMA 3 70B)\
-   Streamlit (frontend demo)

------------------------------------------------------------------------

## 📂 Project Structure

```
    .
    ├── demo/
    │   └── streamlit_app.py
    ├── evaluation/
    │   ├── evaluator.py
    │   └── test_queries.json
    ├── scripts/
    │   ├── build_index.py
    │   ├── run_evaluation.py
    │   └── run_graph.py
    └── src/
        └── course_planner_agent/
            ├── graph/
            ├── ingestion/
            ├── nodes/
            ├── prompts/
            ├── schemas/
            ├── utils/
            └── vectorstore/
```
------------------------------------------------------------------------

## ⚙️ Setup Instructions

### 1. Clone Repository

``` bash
git clone https://github.com/Sumit-Prasad01/CoursePilot-AI.git
```

### 2. Create Virtual Environment

``` bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4. Add API Key

Create `.env` file:
```
    GROQ_API_KEY=your_api_key_here
```
------------------------------------------------------------------------

## 📊 Running the Project

### 1. Build Index

``` bash
python scripts/build_index.py
```

### 2. Run CLI

``` bash
python scripts/run_graph.py
```

### 3. Run Evaluation

``` bash
python scripts/run_evaluation.py
```

### 4. Run UI

``` bash
streamlit run demo/streamlit_app.py
```

------------------------------------------------------------------------

## 🧪 Example Queries

-   Can I take CS102 if I completed CS101?\
-   What do I need before CS401?\
-   What is the maximum credit limit?\
-   Is CS301 offered in Fall?

------------------------------------------------------------------------

## 📌 Example Output

    Answer / Plan:
    CS201 with a grade of B or above

    Why:
    CS401 requires CS201 with minimum grade B

    Citations:
    [Chunk 23]

    Assumptions:
    None

------------------------------------------------------------------------

## 📊 Evaluation Metrics

-   Accuracy (Ground Truth)\
-   Citation Coverage\
-   Abstention Accuracy\
-   Reasoning Completeness

------------------------------------------------------------------------

## 🚫 Safety

-   No hallucination (strict grounding)\
-   Abstains when information not present\
-   Enforced via verifier agent

------------------------------------------------------------------------

## 🧠 Design Decisions

-   LangGraph for modular agent orchestration\
-   FAISS for fast local retrieval\
-   JSON structured outputs for reliability\
-   Verifier node to enforce correctness

------------------------------------------------------------------------

## 🚀 Future Improvements

-   Reranking (Cross-Encoder)\
-   Chat memory\
-   Streaming responses\
-   UI enhancements

------------------------------------------------------------------------

