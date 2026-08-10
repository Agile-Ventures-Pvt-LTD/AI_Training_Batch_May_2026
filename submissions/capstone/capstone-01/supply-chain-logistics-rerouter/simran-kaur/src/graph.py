import json

from langchain import hub

from pydantic import BaseModel, Field
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages


from typing import Annotated, Literal, Sequence
from typing_extensions import TypedDict

from IPython.display import Image, display
from state import LogisticsIncidentState

from src.nodes import parse_incident, policy_rag_lookup, load_alternative_routes, select_route, check_warehouse, analyze_route, route_clarification, finalize_route, escalate_incident, generate_report



workflow = LogisticsIncidentState(state:LogisticsIncidentState)

# Add the nodes
workflow.add_node("parse_incident", parse_incident)
workflow.add_node("policy_rag_lookup", policy_rag_lookup)
workflow.add_node("load_alternative_routes", load_alternative_routes)
workflow.add_node("select_route", select_route)
workflow.add_node("check_warehouse", check_warehouse)
workflow.add_node("analyze_route", analyze_route)
workflow.add_node("finalize_route", finalize_route)
workflow.add_node("escalate_incident", escalate_incident)
workflow.add_node("generate_report", generate_report)

# Define the starting point
workflow.add_edge(START, "parse_incident")
workflow.add_edge("parse_incident", "policy_rag_lookup")
workflow.add_edge("policy_rag_lookup", "load_alternative_routes")
workflow.add_edge("load_alternative_routes", "select_route")
workflow.add_edge("select_route", "check_warehouse")
workflow.add_edge("check_warehouse", "analyze_route")



# Define the routing logic
workflow.add_conditional_edges(
    "analyse_route",  # Branch decisions are made *after* classify_query
    routing_decision,       # The function that decides which branch to take
    {
        # Map the return values of route_query to the names of the next nodes
        "OPTIMAL_PATH_FOUND": "finalize_route",
        "ROUTE_CLARIFICATION": "route_clarification",
        "CRITICAL_DELAY": "escalate_incident"
    }
)

# Define the end points for each branch
workflow.add_edge("finalize_route", "generate_report")
workflow.add_edge("generate_report", END)
workflow.add_edge("escalate_incident", "generate_report")
workflow.add_edge("generate_report", END)

# Compile the graph into a runnable object
compiled_workflow = workflow.compile()


