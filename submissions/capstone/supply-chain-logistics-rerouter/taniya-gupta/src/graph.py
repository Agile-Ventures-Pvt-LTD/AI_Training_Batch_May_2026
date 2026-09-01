from langgraph.graph import StateGraph, END
from state import LogisticsIncidentState
from nodes import(
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

def route_after_analysis(state: LogisticsIncidentState):
    decision = state.get("routing_decision")
    if decision == "OPTIMAL_PATH_FOUND":
        return "finalize_route"
    elif decision == "ROUTE_CLARIFICATION":
        return "route_clarification"
    else:
        return "escalate_incident"

def route_after_clarification(state: LogisticsIncidentState):
    decision = state.get("routing_decision")
    if decision == "ROUTE_CLARIFICATION":
        return "select_route"
    else:
        return "escalate_incident"
    
workflow=StateGraph(LogisticsIncidentState)
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

#this is the starting point of the graph
workflow.set_entry_point("parse_incident")

workflow.add_edge("parse_incident", "policy_rag_lookup")
workflow.add_edge("policy_rag_lookup", "load_alternative_routes")
workflow.add_edge("load_alternative_routes", "select_route")
workflow.add_edge("select_route", "check_warehouse")
workflow.add_edge("check_warehouse","analyze_route")

# these are conditional edges
workflow.add_conditional_edges(
   "analyze_route",
   route_after_analysis,
   {
       "finalize_route": "finalize_route",
       "route_clarification" : "route_clarification",
       "escalate_incident" : "escalate_incident"
   } 
)

workflow.add_conditional_edges(
    "route_clarification",
    route_after_clarification,
    {
        "select_route" : "select_route",
        "escalate_incident" : "escalate_incident"
    }
)

workflow.add_edge("finalize_route", "generate_report")
workflow.add_edge("escalate_incident", "generate_report")
workflow.add_edge("generate_report", END)

app= workflow.compile()