from typing import Dict, Any

from src.course_planner_agent.graph.builder import build_graph
from src.course_planner_agent.utils.logger import logger


class CoursePlannerWorkflow:
    def __init__(self):
        self.app = build_graph()

    def run(self, query: str) -> Dict[str, Any]:
        """
        Execute the LangGraph workflow
        """
        try:
            logger.info("Starting workflow execution")

            initial_state = {
                "query": query
            }

            result = self.app.invoke(initial_state)

            logger.info("Workflow execution completed")

            return {
                "final_output": result.get("final_output"),
                "citations": result.get("citations"),
                "clarifying_questions": result.get("clarifying_questions"),
                "error": result.get("error")
            }

        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {
                "final_output": None,
                "error": str(e)
            }