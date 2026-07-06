from langgraph.graph import StateGraph, END 
from src.state import LogisticsIncidentState 
from src.nodes import ( parse_incident, policy_rag_lookup, load_alternative_routes, select_route, check_warehouse, analyze_route, route_clarification, finalize_route, escalate_incident, generate_report) 

def choose_next_step(state: LogisticsIncidentState) -> str : 
    """Choose graph path after route analysis.""" 
    decision = state["routing_decision"] 
    if decision == "OPTIMAL_PATH_FOUND": 
        return "finalize_route"
    if decision == "ROUTE_CLARIFICATION": 
        return "route_clarification" 
    return "escalate_incident" 

def after_clarification(state: LogisticsIncidentState) -> str: 
    """Check whether another route is available.""" 
    if state["routing_decision"] == "CRITICAL_DELAY": 
        return "escalate_incident" 
    return "select_route" 

def build_graph(): 
    graph = StateGraph(LogisticsIncidentState)
    graph.add_node("parse_incident", parse_incident) 
    graph.add_node("load_alternative_routes",load_alternative_routes)
    graph.add_node("policy_rag_lookup", policy_rag_lookup) 
    graph.add_node("select_route", select_route) 
    graph.add_node("check_warehouse", check_warehouse) 
    graph.add_node("analyze_route", analyze_route) 
    graph.add_node("route_clarification", route_clarification) 
    graph.add_node("finalize_route", finalize_route) 
    graph.add_node("escalate_incident", escalate_incident)
    graph.add_node("generate_report", generate_report) 

    graph.set_entry_point("parse_incident") 
    graph.add_edge("parse_incident", "policy_rag_lookup") 
    graph.add_edge("policy_rag_lookup", "load_alternative_routes") 
    graph.add_edge("load_alternative_routes", "select_route") 
    graph.add_edge("select_route", "check_warehouse") 
    graph.add_edge("check_warehouse", "analyze_route")  

    graph.add_conditional_edges( "analyze_route", choose_next_step, { "finalize_route": "finalize_route", "route_clarification": "route_clarification", "escalate_incident": "escalate_incident", }, ) 
    graph.add_conditional_edges( "route_clarification", after_clarification, { "select_route": "select_route", "escalate_incident": "escalate_incident", }, )
    graph.add_edge("finalize_route", "generate_report") 
    graph.add_edge("escalate_incident", "generate_report") 
    graph.add_edge("generate_report", END) 
    return graph.compile()

graph_agent = build_graph()


