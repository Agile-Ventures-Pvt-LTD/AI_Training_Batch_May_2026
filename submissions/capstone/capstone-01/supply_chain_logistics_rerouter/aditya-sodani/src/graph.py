from langgraph.graph import StateGraph, END

from state import LogisticsIncidentState

from nodes import (
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


def decide_next_step(state):

    decision = state["routing_decision"]

    if decision == "OPTIMAL_PATH_FOUND":
        return "finalize"

    elif decision == "ROUTE_CLARIFICATION":
        return "retry"

    else:
        return "escalate"


def after_retry(state):

    if state["routing_decision"] == "CRITICAL_DELAY":
        return "escalate"

    return "select"



def build_graph():

    workflow = StateGraph(LogisticsIncidentState)

    workflow.add_node(
        "parse_incident",
        parse_incident
    )

    workflow.add_node(
        "policy_rag_lookup",
        policy_rag_lookup
    )

    workflow.add_node(
        "load_routes",
        load_alternative_routes
    )

    workflow.add_node(
        "select_route",
        select_route
    )

    workflow.add_node(
        "check_warehouse",
        check_warehouse
    )

    workflow.add_node(
        "analyze_route",
        analyze_route
    )

    workflow.add_node(
        "route_clarification",
        route_clarification
    )

    workflow.add_node(
        "finalize",
        finalize_route
    )

    workflow.add_node(
        "escalate",
        escalate_incident
    )

    workflow.add_node(
        "generate_report",
        generate_report
    )


    workflow.set_entry_point(
        "parse_incident"
    )

    workflow.add_edge(
        "parse_incident",
        "policy_rag_lookup"
    )

    workflow.add_edge(
        "policy_rag_lookup",
        "load_routes"
    )

    workflow.add_edge(
        "load_routes",
        "select_route"
    )

    workflow.add_edge(
        "select_route",
        "check_warehouse"
    )

    workflow.add_edge(
        "check_warehouse",
        "analyze_route"
    )

    workflow.add_conditional_edges(
        "analyze_route",
        decide_next_step,
        {
        "finalize":"finalize",
        "retry":"route_clarification",
        "escalate":"escalate"
        }
    )

    workflow.add_conditional_edges(
        "route_clarification",
        after_retry,
        {
        "select":"select_route",
        "escalate":"escalate"
        }
    )

    workflow.add_edge(
        "finalize",
        "generate_report"
    )

    workflow.add_edge(
        "escalate",
        "generate_report"
    )

    workflow.add_edge(
        "generate_report",
        END
    )

    return workflow.compile()
 