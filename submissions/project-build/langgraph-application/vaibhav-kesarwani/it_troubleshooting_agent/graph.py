from langgraph.graph import END, StateGraph, START
from custom_agent import (
    TroubleshootingState,
    agent,
    classify_issue_node,
    retrieve_guidance_node,
    parallel_context_node,
    diagnostic_decision_node,
    resolution_planner_node,
    safety_review_node,
    final_response_node
)

workflow = StateGraph(TroubleshootingState)

workflow.add_node("agent", agent)
workflow.add_node("classify", classify_issue_node)
workflow.add_node("retrieve", retrieve_guidance_node)
workflow.add_node("context", parallel_context_node)
workflow.add_node("diagnostic", diagnostic_decision_node)
workflow.add_node("resolution", resolution_planner_node)
workflow.add_node("safety", safety_review_node)
workflow.add_node("final", final_response_node)

workflow.add_edge(START, "agent")
workflow.add_edge("agent", "classify")
workflow.add_edge("agent", "context")
workflow.add_edge("agent", "retrieve")
workflow.add_edge("agent", "diagnostic")

workflow.add_edge("retrieve", "safety")
workflow.add_edge("retrieve", "resolution")

workflow.add_edge("resolution", "final")
workflow.add_edge("final", END)

try:
    graph = workflow.compile()
except Exception as e:
    print(e)