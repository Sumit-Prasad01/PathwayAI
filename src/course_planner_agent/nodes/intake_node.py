import re
from typing import Dict, Any

from src.course_planner_agent.state.state import GraphState
from src.course_planner_agent.utils.logger import logger
from src.course_planner_agent.schemas.student_profile import StudentProfile


def intake_node(state: GraphState) -> GraphState:
    try:
        logger.info("Running Intake Node")

        query = state.get("query", "")

        # ALWAYS define courses first
        courses = re.findall(r"[A-Z]{2,4}\d{3}", query)

        student_profile = StudentProfile(
            raw_query=query,
            completed_courses=courses if courses else [],
            grades={},
            target_program=None,
            max_credits=None
        )

        state["student_profile"] = student_profile.dict()

        logger.info(f"Extracted student profile: {student_profile}")

        return state

    except Exception as e:
        logger.error(f"Intake Node failed: {e}")
        state["error"] = str(e)
        return state