from functools import partial
from nodes import *
from langgraph.graph import StateGraph, START, END

def route_after_analysis(state: LogisticsIncidentState) -> str:
    decision = state.get("routing_decision", "")
    if decision == "OPTIMAL_PATH_FOUND":
        return "OPTIMAL_PATH_FOUND"
    elif decision == 'CRITICAL_DELAY':
        return "CRITICAL_DELAY"
    elif decision == 'ROUTE_CLARIFICATION':
        return 'ROUTE_CLARIFICATION'
    return "CRITICAL_DELAY"

def route_after_clarification(state: LogisticsIncidentState) -> str:
    decision = state.get("routing_decision", '')
    if decision == 'CRITICAL_DELAY':
        return "CRITICAL_DELAY"
    return "SELECT_ROUTE"

def build_graph(llm, rag):
    graph = StateGraph(LogisticsIncidentState)

    # 1. Register all nodes correctly 
    graph.add_node("parse_incident", parse_incident)
    
    # Pre-inject rag because policy_rag_lookup(state, rag) demands it
    graph.add_node("policy_rag_lookup", partial(policy_rag_lookup, rag=rag))
    
    graph.add_node("load_alternative_routes", load_alternative_routes)
    
    # Added safely without partial because these functions only accept 'state'
    graph.add_node("select_route", select_route)
    graph.add_node("check_warehouse", check_warehouse)
    graph.add_node("analyze_route", analyze_route)
    
    graph.add_node("route_clarification", route_clarification)
    graph.add_node('finalize_route', finalize_route)
    graph.add_node('escalate_incident', escalate_incident)
    graph.add_node('generate_report', generate_report)

    # 2. Set the starting entry point
    graph.set_entry_point("parse_incident")

    # 3. Define sequential pipeline flow
    graph.add_edge("parse_incident", "policy_rag_lookup")
    graph.add_edge("policy_rag_lookup", "load_alternative_routes")
    graph.add_edge("load_alternative_routes", "select_route")
    graph.add_edge("select_route", "check_warehouse")
    graph.add_edge("check_warehouse", "analyze_route")

    # 4. Conditional branching logic from analyze_route
    graph.add_conditional_edges(
        "analyze_route",
        route_after_analysis,
        {
            "OPTIMAL_PATH_FOUND": "finalize_route",
            "ROUTE_CLARIFICATION": "route_clarification",
            "CRITICAL_DELAY": "escalate_incident"
        }
    )

    # 5. Conditional branching logic from route_clarification
    graph.add_conditional_edges(
        "route_clarification",
        route_after_clarification,
        {
            "SELECT_ROUTE": "select_route",
            "CRITICAL_DELAY": "escalate_incident"
        }
    )

    # 6. Tie up finishing nodes
    graph.add_edge('finalize_route', 'generate_report')
    graph.add_edge('escalate_incident', 'generate_report')
    graph.add_edge('generate_report', END)

    compiled = graph.compile()
    return compiled
