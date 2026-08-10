from langgraph.graph import START, END, StateGraph
from src.state import LogisticsIncidentState

from src.nodes import (
    parse_incident,
    policy_rag_lookup,
    load_alternative_routes,
    select_route,
    check_warehouse,
    analyze_route,
    route_clarification,
    finalize_route,
    escalate_incident,
    generate_report,
)

def route_after_analysis(state: LogisticsIncidentState) -> str:
    """Decide next step based on analyze_route output."""
    decision = (state.get("routing_decision") or "").upper()
    if decision == "CRITICAL_DELAY":
        return "route_clarification"
    return "finalize_route"


def route_after_clarification(state: LogisticsIncidentState) -> str:
    decision = (state.get("routing_decision") or "").upper()
    if decision == "ESCALATE":
        return "escalate_incident"
    return "select_route"


graph = StateGraph(LogisticsIncidentState)

graph.add_node("parse_incident", parse_incident)
graph.add_node("policy_rag_lookup", policy_rag_lookup)
graph.add_node("load_alternative_routes", load_alternative_routes)
graph.add_node("select_route", select_route)
graph.add_node("check_warehouse", check_warehouse)
graph.add_node("analyze_route", analyze_route)
graph.add_node("route_clarification", route_clarification)
graph.add_node("finalize_route", finalize_route)
graph.add_node("escalate_incident", escalate_incident)
graph.add_node("generate_report", generate_report)

graph.add_edge(START, "parse_incident")
graph.add_edge("parse_incident", "policy_rag_lookup")
graph.add_edge("policy_rag_lookup", "load_alternative_routes")
graph.add_edge("load_alternative_routes", "select_route")
graph.add_edge("select_route", "check_warehouse")
graph.add_edge("check_warehouse", "analyze_route")

graph.add_conditional_edges(
    "analyze_route",
    route_after_analysis,
    {
        "route_clarification": "route_clarification",
        "finalize_route": "finalize_route",
    },
)

graph.add_edge("finalize_route", "generate_report")

graph.add_conditional_edges(
    "route_clarification",
    route_after_clarification,
    {
        "select_route": "select_route",
        "escalate_incident": "escalate_incident",
    },
)

graph.add_edge("escalate_incident", "generate_report")
graph.add_edge("generate_report", END)
compiled_graph = graph.compile()


