import streamlit as st
from dotenv import load_dotenv

from src.course_planner_agent.graph.workflow import CoursePlannerWorkflow

load_dotenv()

st.set_page_config(page_title="CoursePilot AI", layout="wide")

st.title("🎓 CoursePilot AI")
st.markdown("AI-powered Course Planning Assistant (RAG + LangGraph)")

# Initialize workflow
if "workflow" not in st.session_state:
    st.session_state.workflow = CoursePlannerWorkflow()

query = st.text_area("Enter your query:", height=120)

if st.button("Run"):
    if query.strip() == "":
        st.warning("Please enter a query.")
    else:
        with st.spinner("Processing..."):
            result = st.session_state.workflow.run(query)

        final = result.get("final_output")

        # Safe handling (no crash)
        if isinstance(final, dict):
            st.subheader("📌 Answer")

            # Clean structured display
            st.markdown(final.get("answer", ""))

            # Optional sections
            if final.get("why"):
                st.markdown("### 🤔 Why")
                st.markdown(final["why"])

            if final.get("clarifying_questions"):
                st.markdown("### ❓ Clarifying Questions")
                for q in final["clarifying_questions"]:
                    st.markdown(f"- {q}")

            if final.get("assumptions"):
                st.markdown("### ⚠️ Assumptions")
                st.markdown(final["assumptions"])

        elif isinstance(final, str):
            st.subheader("📌 Answer")
            st.markdown(final)

        else:
            st.warning("No output generated")

        # Clean citations display
        citations = result.get("citations", [])

        if citations:
            st.markdown("### 📚 Citations")
            for c in citations:
                st.markdown(f"- {c}")

        # Error handling
        if result.get("error"):
            st.error(result["error"])