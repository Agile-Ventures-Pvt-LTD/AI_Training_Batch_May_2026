from langgraph.graph import StateGraph, START, END

from state import LogisticsIncidentState
from nodes import (
    parse_incident,
    retrieve_Logistics_rules,
    load_alternative_routes,
    select_route,
    check_assigned_warehouse,
    analyze_route,
    route_clarification,
    finalize_route,
    escalate_incident,
    generate_report,
)


# Decide - where to go after analyze_route

def routing_condition(state):
    return state["routing_decision"]


# Decide - whether to retry or escalate
def clarification_condition(state):
    if state["routing_decision"] == "CRITICAL_DELAY":
        return "ESCALATE"

    return "NEXT_ROUTE"

builder = StateGraph(LogisticsIncidentState)

# ---------------- Nodes ----------------

builder.add_node("parse_incident", parse_incident)
builder.add_node("retrieve_Logistics_rules", retrieve_Logistics_rules)
builder.add_node("load_alternative_routes", load_alternative_routes,)
builder.add_node("select_route", select_route)
builder.add_node("check_assigned_warehouse", check_assigned_warehouse)
builder.add_node("analyze_route", analyze_route)
builder.add_node("route_clarification", route_clarification,)
builder.add_node("finalize_route", finalize_route)
builder.add_node("escalate_incident", escalate_incident,)
builder.add_node("generate_report", generate_report,)

#  Flow

builder.add_edge(START, "parse_incident",)
builder.add_edge("parse_incident", "retrieve_Logistics_rules",)
builder.add_edge("retrieve_Logistics_rules", "load_alternative_routes",)
builder.add_edge("load_alternative_routes", "select_route",)
builder.add_edge("select_route", "check_assigned_warehouse",)
builder.add_edge("check_assigned_warehouse", "analyze_route",)

#  Decision 
builder.add_conditional_edges("analyze_route", routing_condition,
    {
        "OPTIMAL_PATH_FOUND": "finalize_route",
        "ROUTE_CLARIFICATION": "route_clarification",
        "CRITICAL_DELAY": "escalate_incident",
    },
)

#  Retry Loop 
builder.add_conditional_edges("route_clarification", clarification_condition,
    {
        "NEXT_ROUTE": "select_route",
        "ESCALATE": "escalate_incident",
    },
)

builder.add_edge("finalize_route","generate_report",)
builder.add_edge("escalate_incident", "generate_report",)
builder.add_edge("generate_report", END,)

app = builder.compile()
