from src.rag import get_relevant_rules_text as get_relevant_rules
from src.tools import (
    get_alternative_routes_tool,
    query_warehouse_inventory_tool,
    extract_shipment_metadata,
    generate_operations_brief,
)
from src.report_writer import build_report

def parse_incident(state: dict) -> dict:
    metadata = extract_shipment_metadata(state["manifest_text"])
    state["extracted_metadata"] = metadata.model_dump()
    return state

def policy_rag_lookup(state: dict) -> dict:
    metadata = state["extracted_metadata"]
    query = (
        f"Cargo Type: {metadata['cargo_type']} "
        f"Cargo Weight: {metadata['cargo_weight_tons']} "
        f"Warehouse: {metadata['target_warehouse_id']}"
    )
    state["routing_rag_context"] = get_relevant_rules(query)
    return state

def load_alternative_routes(state: dict) -> dict:
    state["available_routes"] = get_alternative_routes_tool(state["disrupted_port_id"])
    state["current_route_index"] = 0
    state["clarification_attempts"] = 0
    state["evaluated_routes"] = []
    return state

def select_route(state: dict) -> dict:
    routes = state["available_routes"]
    index = state["current_route_index"]
    if index >= len(routes):
        state["routing_decision"] = "CRITICAL_DELAY"
        state["selected_route"] = {}
        return state
    state["selected_route"] = routes[index]
    return state

def check_warehouse(state: dict) -> dict:
    warehouse_id = state["selected_route"]["warehouse_id"]
    state["warehouse_db_context"] = query_warehouse_inventory_tool(warehouse_id)
    return state

def analyze_route(state: dict) -> dict:
    metadata = state["extracted_metadata"]
    route = state["selected_route"]
    warehouse = state["warehouse_db_context"]

    utilization_high = warehouse.get("current_utilization_pct", 0) > 85
    risk_elevated = warehouse.get("risk_tier", "NORMAL") == "ELEVATED"
    warehouse_inactive = warehouse.get("operational_status", "ACTIVE") != "ACTIVE"
    delay = route.get("added_delay_hours", 0)
    tolerance = metadata.get("maximum_tolerable_delay_hours")
    exceeds_tolerance = tolerance is not None and delay > tolerance
    critical_delay = delay > 120

    state["reroute_impact_score"] = min(
        100,
        30 * utilization_high
        + 25 * risk_elevated
        + 30 * warehouse_inactive
        + 25 * exceeds_tolerance
        + 50 * critical_delay,
    )

    if critical_delay:
        decision, reason = "CRITICAL_DELAY", "Added route delay exceeds 120 hours."
    elif utilization_high:
        decision, reason = "ROUTE_CLARIFICATION", "Warehouse utilization above 85 percent."
    elif warehouse_inactive:
        decision, reason = "ROUTE_CLARIFICATION", "Warehouse is not active."
    elif risk_elevated:
        decision, reason = "ROUTE_CLARIFICATION", "Warehouse risk tier is elevated."
    elif exceeds_tolerance:
        decision, reason = "ROUTE_CLARIFICATION", "Route delay exceeds shipment tolerance."
    else:
        decision, reason = "OPTIMAL_PATH_FOUND", "Warehouse and route conditions are acceptable."

    state["routing_decision"] = decision
    state["evaluated_routes"].append(
        {"route_id": route["route_id"], "decision": decision, "reason": reason}
    )
    return state

def route_clarification(state: dict) -> dict:
    state["clarification_attempts"] += 1
    state["current_route_index"] += 1

    out_of_attempts = state["clarification_attempts"] > state["max_clarification_attempts"]
    out_of_routes = state["current_route_index"] >= len(state["available_routes"])
    if out_of_attempts or out_of_routes:
        state["routing_decision"] = "CRITICAL_DELAY"
    return state

def finalize_route(state: dict) -> dict:
    return state

def escalate_incident(state: dict) -> dict:
    state["selected_route"] = {}
    return state

def generate_report(state: dict) -> dict:
    brief = generate_operations_brief(state)
    state["final_report"] = build_report(state, brief)
    return state
