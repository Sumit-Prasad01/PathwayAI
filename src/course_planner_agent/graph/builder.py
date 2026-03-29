from langgraph.graph import StateGraph, END

from src.course_planner_agent.state.state import GraphState
from src.course_planner_agent.nodes.intake_node import intake_node
from src.course_planner_agent.nodes.retrieve_node import retrieve_node
from src.course_planner_agent.nodes.planner_node import planner_node
from src.course_planner_agent.nodes.verifier_node import verifier_node


def build_graph():
    """
    Build LangGraph workflow
    """

    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("intake", intake_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("verifier", verifier_node)

    # Define flow
    workflow.set_entry_point("intake")

    workflow.add_edge("intake", "retrieve")
    workflow.add_edge("retrieve", "planner")
    workflow.add_edge("planner", "verifier")
    workflow.add_edge("verifier", END)

    return workflow.compile()