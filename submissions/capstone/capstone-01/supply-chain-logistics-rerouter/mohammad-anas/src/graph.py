from langgraph.graph import StateGraph, END
from state import LogisticsIncidentState
from nodes import (
    load_alternative_routes,
    parse_incident,
    policy_rag_lookup,
    select_route,
    check_warehouse,
    analyze_route,
    route_clarification,
    finalize_route,
    escalate_incident,
    generate_report
)

def build_incident_graph()->StateGraph[LogisticsIncidentState]:
    graph = StateGraph(LogisticsIncidentState)
    
    graph.add_node("parse_incident",parse_incident)
    graph.add_node("policy_rag_lookup",policy_rag_lookup)
    graph.add_node("load_alternative_routes",load_alternative_routes)
    graph.add_node("select_route",select_route)
    graph.add_node("check_warehouse",check_warehouse)
    graph.add_node("analyze_route",analyze_route)
    graph.add_node("route_clarification",route_clarification)
    graph.add_node("finalize_route",finalize_route)
    graph.add_node("escalate_incident",escalate_incident)
    graph.add_node("generate_report",generate_report)
    
    graph.add_edge("parse_incident","policy_rag_lookup")
    graph.add_edge("policy_rag_lookup","load_alternative_routes")
    graph.add_edge("load_alternative_routes","select_route")
    graph.add_edge("select_route","check_warehouse")
    graph.add_edge("check_warehouse","analyze_route")
    
    graph.add_conditional_edges("analyze_route", lambda s : s["routing_decision"],{
        "OPTIMAL_PATH_FOUND":"finalize_route",
        "ROUTE_CLARIFICATION":"route_clarification",
        "CRITICAL_DELAY":"escalate_incident"
    },)
    graph.add_edge("route_clarification","select_route")
    graph.add_edge("finalize_route","generate_report")
    graph.add_edge("escalate_incident","generate_report")
    
    graph.add_edge("generate_report",END)
    
agent_app = build_incident_graph()