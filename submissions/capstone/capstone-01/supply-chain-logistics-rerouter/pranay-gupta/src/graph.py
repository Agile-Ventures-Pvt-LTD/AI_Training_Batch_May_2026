from langgraph.graph import StateGraph, START, END

from src.state import LogisticsIncidentState
from src.nodes import (parse_incident,policy_rag_lookup,load_alternative_routes,select_route,check_warehouse,analyze_route,route_clarification,
                       finalize_route,escalate_incident,generate_report,route_decision_router,clarification_router,select_route_router,
                       configure_dependencies)

def build_workflow(llm=None,retriever=None):
    configure_dependencies(llm=llm,retriever=retriever)
    workflow = StateGraph(LogisticsIncidentState)

    workflow.add_node("parse_incident",parse_incident)
    workflow.add_node("policy_rag_lookup",policy_rag_lookup)
    workflow.add_node("load_alternative_routes",load_alternative_routes)
    workflow.add_node("select_route",select_route)
    workflow.add_node("check_warehouse",check_warehouse)
    workflow.add_node("analyze_route",analyze_route)
    workflow.add_node("route_clarification",route_clarification)
    workflow.add_node("finalize_route",finalize_route)
    workflow.add_node("escalate_incident",escalate_incident)
    workflow.add_node("generate_report",generate_report)

    workflow.add_edge(START,"parse_incident")
    workflow.add_edge("parse_incident","policy_rag_lookup")
    workflow.add_edge("policy_rag_lookup","load_alternative_routes")
    workflow.add_edge("load_alternative_routes","select_route")

    workflow.add_conditional_edges(
        "select_route",
        select_route_router,
        {
            "check_warehouse":"check_warehouse",
            "escalate":"escalate_incident",
        },
    )

    workflow.add_edge("check_warehouse","analyze_route")

    workflow.add_conditional_edges(
        "analyze_route",
        route_decision_router,
        {
            "OPTIMAL_PATH_FOUND": "finalize_route",
            "ROUTE_CLARIFICATION": "route_clarification",
            "CRITICAL_DELAY": "escalate_incident",
        },
    )

    workflow.add_conditional_edges(
        "route_clarification",
        clarification_router,
        {
            "retry":"select_route",
            "escalate":"escalate_incident",
        }
    )

    workflow.add_edge("finalize_route", "generate_report")
    workflow.add_edge("escalate_incident", "generate_report")
    workflow.add_edge("generate_report",END)

    return workflow.compile()

