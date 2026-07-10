# nodes.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from src.schemas import ShipmentMetadata
from src.tools import (query_warehouse_inventory_tool, get_alternative_routes_tool)
import os
from src.rag import retrieve_rules

load_dotenv()

os.environ['GROQ_MODEL'] = os.getenv("GROQ_MODEL")
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model=os.environ['GROQ_MODEL'],
    api_key=os.environ['GROQ_API_KEY'],
    temperature=0
)

# parse - incident 
def parse_incident(state):

    structured_llm = llm.with_structured_output(ShipmentMetadata)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract shipment information from the incident. Return only the required fields."),
        ("human", "{manifest}")
    ])

    chain = prompt | structured_llm

    metadata = chain.invoke({"manifest": state["manifest_text"]})

    state["extracted_metadata"] = metadata.model_dump()
    state.setdefault("logs", []).append("Incident parsed")

    return state

# RAG retrieval
def retrieve_Logistics_rules(state):

    metadata = state["extracted_metadata"]

    query = f"""
    Cargo : {metadata['cargo_type']}
    Weight : {metadata['cargo_weight_tons']}
    Warehouse : {metadata['target_warehouse_id']}
    Delay : {metadata['maximum_tolerable_delay_hours']}
    """

    state["routing_rag_context"] = retrieve_rules(query)
    state["logs"].append("RAG lookup completed")

    return state

# Loading Routes
def load_alternative_routes(state):

    routes = get_alternative_routes_tool(state["disrupted_port_id"])

    state["available_routes"] = routes
    state["current_route_index"] = 0
    state["clarification_attempts"] = 0
    state["max_clarification_attempts"] = 2
    state["routes_evaluated"] = []
    state["logs"].append("Routes loaded")

    return state

# Select Route
def select_route(state):

    index = state["current_route_index"]

    if index >= len(state["available_routes"]):
        state["routing_decision"] = "CRITICAL_DELAY"
        return state

    state["selected_route"] = state["available_routes"][index]

    state["logs"].append(f"Selected route {state['selected_route']['route_id']}")

    return state

# Warehouse Check
def check_assigned_warehouse(state):

    warehouse_id = state["selected_route"]["warehouse_id"]
    warehouse = query_warehouse_inventory_tool(warehouse_id)

    state["warehouse_db_context"] = warehouse
    state["logs"].append(f"Warehouse checked {warehouse_id}")

    return state

# Route Analysis
def analyze_route(state):

    metadata = state["extracted_metadata"]
    warehouse = state["warehouse_db_context"]
    route = state["selected_route"]

    score = 0
    decision = "OPTIMAL_PATH_FOUND"
    reason = "Warehouse and the route conditions are acceptable."

    delay = route["added_delay_hours"]

    max_delay = metadata.get("maximum_tolerable_delay_hours")

    if delay > 120:
        score += 50
        decision = "CRITICAL_DELAY"
        reason = "Route delay exceeds 120 hours."

    elif warehouse.get("current_utilization_pct", 0) > 85:
        score += 30
        decision = "ROUTE_CLARIFICATION"
        reason = "Warehouse utilization above 85%."

    elif warehouse.get("operational_status") != "ACTIVE":
        score += 30
        decision = "ROUTE_CLARIFICATION"
        reason = "Warehouse not ACTIVE."

    elif warehouse.get("risk_tier") == "ELEVATED":
        score += 25
        decision = "ROUTE_CLARIFICATION"
        reason = "Warehouse risk is ELEVATED."

    elif max_delay is not None and delay > max_delay:
        score += 25
        decision = "ROUTE_CLARIFICATION"
        reason = "Shipment delay exceeded."

    state["reroute_impact_score"] = min(score, 100)
    state["routing_decision"] = decision

    state["routes_evaluated"].append(
            {
                "route_id": route["route_id"],
                "decision": decision,
                "reason": reason
            }
        )

    state["logs"].append(reason)

    return state

# Retry Route
def route_clarification(state):

    state["clarification_attempts"] += 1
    state["current_route_index"] += 1

    if (state["clarification_attempts"] >= state["max_clarification_attempts"]):
        state["routing_decision"] = "CRITICAL_DELAY"
        return state

    if (state["current_route_index"] >= len(state["available_routes"])):
        state["routing_decision"] = "CRITICAL_DELAY"

    return state


# Finalize
def finalize_route(state):

    state["logs"].append("Route finalized")

    return state

# Escalate
def escalate_incident(state):

    state["selected_route"] = {}
    state["logs"].append("Incident escalated")

    return state


# Final Report
def generate_report(state):

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Write a short logistics operations in brief within 3-4 lines."),
        ("human",""" Incident: {incident} Decision: {decision} Selected Route: {route} Rules: {rules}""")
    ])

    chain = prompt | llm

    brief = chain.invoke(
        {
            "incident": state["manifest_text"],
            "decision": state["routing_decision"],
            "route": state["selected_route"],
            "rules": state["routing_rag_context"],
        }).content

    state["final_report"] = {
        "incident_id": state["incident_id"],
        "original_incident_summary": state["manifest_text"],
        "parsed_metadata": state["extracted_metadata"],
        "rag_validation_rules_applied":
            state["routing_rag_context"].split("\n"),
        "routes_evaluated":
            state["routes_evaluated"],
        "final_selected_route":
            state["selected_route"],
        "queried_warehouse_metrics":
            state["warehouse_db_context"],
        "graph_routing_metadata": {
            "loops_executed":
                state["clarification_attempts"],
            "final_decision_state":
                state["routing_decision"],
            "reroute_impact_score":
                state["reroute_impact_score"],
        },
        "final_operations_brief":
            brief
    }

    state["logs"].append("Logictic Report Generated")

    return state