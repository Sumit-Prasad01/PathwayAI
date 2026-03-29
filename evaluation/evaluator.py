import json
from typing import Dict, List
from dotenv import load_dotenv

from src.course_planner_agent.graph.workflow import CoursePlannerWorkflow
from src.course_planner_agent.utils.logger import logger


load_dotenv()


def load_test_queries(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate():
    try:
        logger.info("Starting evaluation...")

        workflow = CoursePlannerWorkflow()
        test_cases = load_test_queries("evaluation/test_queries.json")

        total = len(test_cases)
        citation_count = 0
        abstention_count = 0

        results = []

        for test in test_cases:
            query = test["query"]
            q_type = test["type"]

            logger.info(f"Evaluating: {query}")

            output = workflow.run(query)
            final_output = output.get("final_output", "")

            # Check citation presence
            has_citation = "[Chunk" in (final_output or "")
            if has_citation:
                citation_count += 1

            # Check abstention
            is_abstained = "I don’t have" in (final_output or "")
            if q_type == "not_in_docs" and is_abstained:
                abstention_count += 1

            results.append({
                "query": query,
                "type": q_type,
                "has_citation": has_citation,
                "abstained_correctly": is_abstained if q_type == "not_in_docs" else None,
                "output": final_output
            })

        # Metrics
        citation_coverage = (citation_count / total) * 100
        abstention_accuracy = (abstention_count / 5) * 100  # 5 trick questions

        logger.info("\n" + "=" * 50)
        logger.info("EVALUATION RESULTS")
        logger.info("=" * 50)
        logger.info(f"Total Queries: {total}")
        logger.info(f"Citation Coverage: {citation_coverage:.2f}%")
        logger.info(f"Abstention Accuracy: {abstention_accuracy:.2f}%")

        # Save results
        with open("evaluation/results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        logger.info("Evaluation completed")

    except Exception as e:
        logger.error(f"Evaluation failed: {e}")


if __name__ == "__main__":
    evaluate()