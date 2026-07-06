from langgraph.graph import StateGraph, START, END
from src.state import LogisticsIncidentState
from src.nodes import (parse_incident, policy_rag_lookup, load_alternative_routes,select_route, check_warehouse, analyze_route, route_clarification,finalize_route, escalate_incident)
from src.report_writer import generate_report

def route_decision(state: LogisticsIncidentState):
    decision = state["routing_decision"]
    if decision == "OPTIMAL_PATH_FOUND":
        return "finalize_route"
    elif decision == "ROUTE_CLARIFICATION":
        return "route_clarification"
    else:
        return "escalate_incident"

def clarification_router(state: LogisticsIncidentState):
    if state["routing_decision"] == "CRITICAL_DELAY":
        return "escalate_incident"
    return "select_route"

builder = StateGraph(LogisticsIncidentState)

builder.add_node("parse_incident", parse_incident)
builder.add_node("policy_rag_lookup", policy_rag_lookup)
builder.add_node("load_alternative_routes", load_alternative_routes)
builder.add_node("select_route", select_route)
builder.add_node("check_warehouse", check_warehouse)
builder.add_node("analyze_route", analyze_route)
builder.add_node("route_clarification", route_clarification)
builder.add_node("finalize_route", finalize_route)
builder.add_node("escalate_incident", escalate_incident)
builder.add_node("generate_report", generate_report)

builder.add_edge(START, "parse_incident")
builder.add_edge("parse_incident", "policy_rag_lookup")
builder.add_edge("policy_rag_lookup", "load_alternative_routes")
builder.add_edge("load_alternative_routes", "select_route")
builder.add_edge("select_route", "check_warehouse")
builder.add_edge("check_warehouse", "analyze_route")

builder.add_conditional_edges("analyze_route",route_decision,{"finalize_route": "finalize_route","route_clarification": "route_clarification","escalate_incident": "escalate_incident"})

builder.add_conditional_edges("route_clarification",clarification_router,{"select_route": "select_route","escalate_incident": "escalate_incident"})

builder.add_edge("finalize_route", "generate_report")
builder.add_edge("escalate_incident", "generate_report")
builder.add_edge("generate_report", END)

app = builder.compile()
