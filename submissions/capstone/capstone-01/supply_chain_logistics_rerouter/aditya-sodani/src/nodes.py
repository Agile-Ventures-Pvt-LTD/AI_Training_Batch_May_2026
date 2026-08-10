from config import *
from langchain_groq import ChatGroq
from schemas import ShipmentMetadata
from rag import retrieve_rules
from tools import (
    get_alternative_routes_tool,
    query_warehouse_inventory_tool
)

llm = ChatGroq(model=Config.GROQ_MODEL_NAME,api_key=Config.GROQ_API_KEY)

# 1. Parse Incident
def parse_incident(state):
    structured_llm = llm.with_structured_output(
        ShipmentMetadata
    )

    result = structured_llm.invoke(
        f"""
        Extract shipment details.
        Incident:
        {state["manifest_text"]}
        """
    )

    state["extracted_metadata"] = result.model_dump()

    state["logs"].append(
        "Shipment metadata extracted"
    )

    return state


# 2. RAG Lookup
def policy_rag_lookup(state):

    query = state["manifest_text"]

    rules = retrieve_rules(query)

    state["routing_rag_context"] = rules

    state["logs"].append(
        "RAG logistics rules retrieved"
    )

    return state


# 3. Load Alternative Routes
def load_alternative_routes(state):

    routes = get_alternative_routes_tool(
        state["disrupted_port_id"]
    )

    state["available_routes"] = routes
    state["current_route_index"] = 0
    state["clarification_attempts"] = 0
    state["max_clarification_attempts"] = 2
    state["routes_evaluated"] = []

    return state


# 4. Select Route
def select_route(state):

    index = state["current_route_index"]
    routes = state["available_routes"]

    if index < len(routes):
        state["selected_route"] = routes[index]

    else:
        state["selected_route"] = {}
        state["routing_decision"] = "CRITICAL_DELAY"

    return state


# 5. Warehouse Check
def check_warehouse(state):

    route = state["selected_route"]
    warehouse_id = route.get("warehouse_id")

    result = query_warehouse_inventory_tool(warehouse_id)

    state["warehouse_db_context"] = result

    return state



# Helper scoring logic
def calculate_score(route,warehouse,metadata):
    score = 0

    if warehouse.get("current_utilization_pct",0) > 85:
        score += 30

    if warehouse.get("risk_tier") == "ELEVATED":
        score += 25

    if warehouse.get("operational_status") != "ACTIVE":
        score += 30

    max_delay = metadata.get("maximum_tolerable_delay_hours")

    if max_delay:
        if route["added_delay_hours"] > max_delay:
            score += 25

    if route["added_delay_hours"] > 120:
        score += 50

    return min(score,100)


# 6. Analyze Route
def analyze_route(state):
    route = state["selected_route"]
    warehouse = state["warehouse_db_context"]
    metadata = state["extracted_metadata"]
    decision = "OPTIMAL_PATH_FOUND"
    reason = "Warehouse and route conditions are acceptable"

    if route["added_delay_hours"] > 120:
        decision = "CRITICAL_DELAY"
        reason = "Added delay hours is greater than 120"
    elif warehouse.get("current_utilization_pct") > 85:
        decision = "ROUTE_CLARIFICATION"
        reason = "current utilization pct is greater than 85"
    elif warehouse.get("operational_status") != "ACTIVE":
        decision = "ROUTE_CLARIFICATION"
        reason = "operational status is not active"
    elif warehouse.get("risk_tier") == "ELEVATED":
        decision = "ROUTE_CLARIFICATION"
        reason = "Warehouse risk tier is ELEVATED"
    elif metadata.get("maximum_tolerable_delay_hours"):
        if route["added_delay_hours"] > metadata[
            "maximum_tolerable_delay_hours"
        ]:
            decision = "ROUTE_CLARIFICATION"
            reason = "added delay hours are not tolerable"

    expected_reason = reason
    state["routing_decision"] = decision
    state["reroute_impact_score"] = calculate_score(route,warehouse,metadata)

    state["routes_evaluated"].append(
        {
        "route_id":route["route_id"],
        "decision":decision,
        "reason": expected_reason
    }
    )

    return state


# 7. Route Clarification
def route_clarification(state):
    state["clarification_attempts"] += 1
    state["current_route_index"] += 1

    if (state["clarification_attempts"]>state["max_clarification_attempts"]):

        state["routing_decision"] = "CRITICAL_DELAY"

    return state



# 8. Finalize
def finalize_route(state):
    state["logs"].append("Route finalized")

    return state


# 9. Escalation
def escalate_incident(state):
    state["selected_route"] = {}
    state["logs"].append("Incident escalated")

    return state


# 10. Report Node
def generate_report(state):

    response = llm.invoke(
        f"""
        Create short logistics operation brief.
        Decision:
        {state["routing_decision"]}
        Route:
        {state["selected_route"]}
        """
    )

    state["final_report"] = {
        "incident_id":state["incident_id"],
        "parsed_metadata":state["extracted_metadata"],
        "rag_validation_rules_applied":state["routing_rag_context"],
        "routes_evaluated":state["routes_evaluated"],
        "final_selected_route":state["selected_route"],
        "queried_warehouse_metrics":state["warehouse_db_context"],
        "graph_routing_metadata":{
            "loops_executed":state["clarification_attempts"],
            "final_decision_state":state["routing_decision"],
            "reroute_impact_score":state["reroute_impact_score"]
        },
        "final_operations_brief":response.content
    }

    return state
 

