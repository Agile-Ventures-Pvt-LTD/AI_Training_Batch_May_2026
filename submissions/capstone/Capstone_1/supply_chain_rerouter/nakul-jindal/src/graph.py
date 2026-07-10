from typing import Literal
from langgraph.graph import StateGraph, START, END
from src.state import LogisticsIncidentState
from src.nodes import (
    parse_incident, policy_rag_lookup, load_alternative_routes,
    select_route, check_warehouse, analyze_route,
    route_clarification, finalize_route, escalate_incident, generate_report,
)

def route_after_analysis(state: dict) -> Literal["finalize_route", "escalate_incident", "route_clarification"]:
    decision = state["routing_decision"]
    if decision == "OPTIMAL_PATH_FOUND":
        return "finalize_route"
    if decision == "CRITICAL_DELAY":
        return "escalate_incident"
    return "route_clarification"

def route_after_clarification(state: dict) -> Literal["select_route", "escalate_incident"]:
    return "escalate_incident" if state["routing_decision"] == "CRITICAL_DELAY" else "select_route"

def build_graph():
    graph = StateGraph(LogisticsIncidentState)

    for name, fn in [
        ("parse_incident", parse_incident),
        ("policy_rag_lookup", policy_rag_lookup),
        ("load_alternative_routes", load_alternative_routes),
        ("select_route", select_route),
        ("check_warehouse", check_warehouse),
        ("analyze_route", analyze_route),
        ("route_clarification", route_clarification),
        ("finalize_route", finalize_route),
        ("escalate_incident", escalate_incident),
        ("generate_report", generate_report),
    ]:
        graph.add_node(name, fn)

    graph.add_edge(START, "parse_incident")
    graph.add_edge("parse_incident", "policy_rag_lookup")
    graph.add_edge("policy_rag_lookup", "load_alternative_routes")
    graph.add_edge("load_alternative_routes", "select_route")
    graph.add_edge("select_route", "check_warehouse")
    graph.add_edge("check_warehouse", "analyze_route")

    graph.add_conditional_edges("analyze_route", route_after_analysis)
    graph.add_conditional_edges("route_clarification", route_after_clarification)

    graph.add_edge("finalize_route", "generate_report")
    graph.add_edge("escalate_incident", "generate_report")
    graph.add_edge("generate_report", END)

    return graph.compile()
