from langgraph.graph import StateGraph, END
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
    generate_report
)

def select_route_router(state: LogisticsIncidentState) -> str:
    """Route from select_route based on whether a route was successfully selected."""
    
    if state.get("routing_decision") == "CRITICAL_DELAY" or not state.get("selected_route"):
        return "escalate_incident"
    return "check_warehouse"

def analyze_route_router(state: LogisticsIncidentState) -> str:
    """Route from analyze_route based on the routing decision."""
    decision = state.get("routing_decision")
    if decision == "OPTIMAL_PATH_FOUND":
        return "finalize_route"
    elif decision == "ROUTE_CLARIFICATION":
        return "route_clarification"
    else:
        return "escalate_incident"

def route_clarification_router(state: LogisticsIncidentState) -> str:
    """Route from route_clarification based on whether retry is possible."""
    decision = state.get("routing_decision")
    if decision == "ROUTE_CLARIFICATION":
        return "select_route"
    else:
        return "escalate_incident"

def build_workflow() -> StateGraph:
    """Build and compile the LangGraph workflow."""
    workflow = StateGraph(LogisticsIncidentState)
    
    workflow.add_node("parse_incident", parse_incident)
    workflow.add_node("policy_rag_lookup", policy_rag_lookup)
    workflow.add_node("load_alternative_routes", load_alternative_routes)
    workflow.add_node("select_route", select_route)
    workflow.add_node("check_warehouse", check_warehouse)
    workflow.add_node("analyze_route", analyze_route)
    workflow.add_node("route_clarification", route_clarification)
    workflow.add_node("finalize_route", finalize_route)
    workflow.add_node("escalate_incident", escalate_incident)
    workflow.add_node("generate_report", generate_report)
    
    workflow.set_entry_point("parse_incident")
    
    workflow.add_edge("parse_incident", "policy_rag_lookup")
    workflow.add_edge("policy_rag_lookup", "load_alternative_routes")
    workflow.add_edge("load_alternative_routes", "select_route")
    workflow.add_edge("check_warehouse", "analyze_route")
    workflow.add_edge("finalize_route", "generate_report")
    workflow.add_edge("escalate_incident", "generate_report")
    workflow.add_edge("generate_report", END)
    
    workflow.add_conditional_edges(
        "select_route",
        select_route_router,
        {
            "check_warehouse": "check_warehouse",
            "escalate_incident": "escalate_incident"
        }
    )
    
    workflow.add_conditional_edges(
        "analyze_route",
        analyze_route_router,
        {
            "finalize_route": "finalize_route",
            "route_clarification": "route_clarification",
            "escalate_incident": "escalate_incident"
        }
    )
    
    workflow.add_conditional_edges(
        "route_clarification",
        route_clarification_router,
        {
            "select_route": "select_route",
            "escalate_incident": "escalate_incident"
        }
    )
    
    return workflow.compile()
app = build_workflow()
