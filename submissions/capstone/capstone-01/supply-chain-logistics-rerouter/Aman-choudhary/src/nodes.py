import logging
from typing import Any
from src.rag import get_relevant_rules
# from src.report_writer import build_report
from src.rag import ShipmentMetadata
from src.tools import (get_alternative_routes_tool,query_warehouse_inventory_tool,)
from src.tools import (extract_shipment_metadata,generate_operations_brief,)
LOGGER = logging.getLogger(__name__)
def parse_incident(state: dict,)-> dict:
    """
    extract structured shipment metadata 
    """
    metadata = extract_shipment_metadata(state["manifest_text"])
    state["extracted_metadata"] = (metadata.model_dump())
    state["logs"].append("Shipment metadata extracted.")
    return state
def policy_rag_lookup(state: dict,)-> dict:
    """
    retrived logicstic rules to the current incident
    """
    metadata = state["extracted_metadata"]
    query = (f"""Cargo Type: {metadata['cargo_type']}Cargo Weight: {metadata['cargo_weight_tons']}Warehouse: {metadata['target_warehouse_id']}""")
    rag_context = get_relevant_rules(query)
    state["routing_rag_context"] = (rag_context)
    state["logs"].append("relevent logistics")
    return state
def load_alternative_routes(state: dict,)-> dict:
    """
     load routing options
    """
    routes = (get_alternative_routes_tool(state["disrupted_port_id"]))
    state["available_routes"] = routes
    state["current_route_index"] = 0
    state["clarification_attempts"] = 0
    state["logs"].append(f"{len(routes)} routes loaded.")
    return state
def select_route(state: dict,)-> dict:
    """
    Select route using current route index.
    """
    routes = state["available_routes"]
    index = state["current_route_index"]
    if index >= len(routes):
        state["routing_decision"] = ("CRITICAL_DELAY")
        state["selected_route"] = {}
        return state
    selected_route = routes[index]
    state["selected_route"] = (selected_route)
    state["logs"].append(f"Selected route "f"{selected_route['route_id']}")
    return state
def check_warehouse(state: dict,)->dict:
    """
    Query warehouse inventory information.
    """
    route = state["selected_route"]
    warehouse_id = (route["warehouse_id"])
    warehouse_context = (query_warehouse_inventory_tool(warehouse_id))
    state["warehouse_db_context"] = (warehouse_context)
    state["logs"].append(f"Warehouse checked: "f"{warehouse_id}")
    return state
def calculate_impact_score(metadata: dict,route: dict,warehouse: dict,)->int:
    score = 0
    utilization = warehouse.get("current_utilization_pct",0,)
    risk = warehouse.get("risk_tier","NORMAL",)
    status = warehouse.get("operational_status","UNKNOWN",)
    delay_hours = route.get("added_delay_hours",0,)
    shipment_limit = metadata.get("maximum_tolerable_delay_hours")
    if utilization > 85:
        score += 30
    if risk == "elevlated":
        score += 25
    if status != "activate":
        score += 30
    if (shipment_limit is not None and delay_hours > shipment_limit):
        score += 25
    if delay_hours > 120:
        score += 50
    return min(score, 100)
def analyze_route(state: dict,)->dict:
    metadata = state["extracted_metadata"]
    route = state["selected_route"]
    warehouse = state["warehouse_db_context"]
    utilization = warehouse.get("current_utilization_pct",0,)
    risk = warehouse.get("risk_tier","NORMAL",)
    op_status = warehouse.get("operational_status","ACTIVE",)
    delay = route.get("added_delay_hours",0,)
    shipment_limit = metadata.get("maximum_tolerable_delay_hours")
    state["reroute_impact_score"]=calculate_impact_score(metadata,route,warehouse,)
    decision = ("OPTIMAL_PATH_FOUND")
    reason = ("Warehouse and route ""conditions are acceptable.")
    if delay > 120:
        decision = "CRITICAL_DELAY"
        reason = ("Added route delay ","exceeds 120 hours.")
    elif utilization > 85:
        decision = ("ROUTE_CLARIFICATION")
        reason = ("Warehouse utilization ""above 85 percent.")
    elif op_status != "ACTIVE":
        decision = ("ROUTE_CLARIFICATION")
        reason = ("Warehouse not active.")
    elif risk == "ELEVATED":
        decision = ("ROUTE_CLARIFICATION")
        reason = ("Warehouse risk tier ""is elevated.")
    elif (shipment_limit is not None and delay > shipment_limit):
        decision = ("ROUTE_CLARIFICATION")
        reason = ("Route delay exceeds ""shipment tolerance.")
    state["routing_decision"] = decision
    state["evaluated_routes"].append(
        {"route_id":route["route_id"],"decision":decision,"reason":reason,})
    return state
def route_clarification(state: dict,) -> dict:
    """
    Retry next route.
    """
    state["clarification_attempts"] += 1
    state["current_route_index"] += 1
    max_attempts = state["max_clarification_attempts"]
    routes = state["available_routes"]
    if (state["clarification_attempts"]> max_attempts):
        state["routing_decision"]="CRITICAL_DELAY"
        return state
    if (state["current_route_index"]>= len(routes)):
        state["routing_decision"]="CRITICAL_DELAY"
        return state
    state["routing_decision"]="RETRY_ROUTE"
    return state
def finalize_route(state: dict,) -> dict:
    """
    Accept route.
    """
    state["logs"].append(f"Route finalized: "f"{state['selected_route']['route_id']}")
    return state
def escalate_incident(state: dict,) -> dict:
    """
    Escalate incident.
    """
    state["logs"].append("Incident escalated.")
    state["selected_route"] = {}
    return state
def generate_report(state: dict,) -> dict:
    """
    Final report node.
    """
    brief = generate_operations_brief(state)
    report = build_report(state=state,operations_brief=brief,)
    state["final_report"] = report
    return state