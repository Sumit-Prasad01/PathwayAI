import sys
from dotenv import load_dotenv

from src.course_planner_agent.graph.workflow import CoursePlannerWorkflow
from src.course_planner_agent.utils.logger import logger


load_dotenv()


def main():
    try:
        logger.info("Starting Course Planner")

        workflow = CoursePlannerWorkflow()

        # Get query
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
        else:
            query = input("Enter your query: ")

        result = workflow.run(query)

        logger.info("\n" + "=" * 50)
        logger.info("FINAL OUTPUT:\n")

        final = result.get("final_output")

        if isinstance(final, dict):
            logger.info(final.get("answer", "No answer"))
        elif isinstance(final, str):
            logger.info(final)
        else:
            logger.info("No output generated")

        logger.info("\n" + "=" * 50)

        if result.get("error"):
            logger.error(f"ERROR: {result['error']}")

    except Exception as e:
        logger.error(f"Run failed: {e}")


if __name__ == "__main__":
    main()