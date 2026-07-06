import logging
from typing import Any, Dict, List
from src.tools import (query_warehouse_inventory_tool,get_alternative_routes_tool,get_route_by_id,)
from src.state import LogisticsIncidentState
LOGGER = logging.getLogger(__name__)
def load_warehouse_context(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Step 1:
    Load warehouse information 
    """
    warehouse_id = state["extracted_metadata"].get("warehouse_id")
    if not warehouse_id:
        state["warehouse_db_context"] = {"error": True,"message": "No warehouse_id found in extracted metadata."}
        state["logs"].append("Warehouse lookup skipped: No warehouse_id.")
        return state
    result = query_warehouse_inventory_tool(warehouse_id)
    state["warehouse_db_context"] = result
    state["logs"].append(f"Loaded warehouse context for {warehouse_id}.")
    return state
def load_available_routes(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Step 2:
    Load possible alternative
    """
    disrupted_port = state["disrupted_port_id"]
    routes = get_alternative_routes_tool(disrupted_port)
    state["available_routes"] = routes
    state["current_route_index"] = 0
    state["logs"].append(f"Loaded {len(routes)} routes for {disrupted_port}.")
    return state
def evaluate_routes(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Step 3:
    A simple scoring logic for now:
    • Fewer ETA days = better
    • Fallback if missing ETA
    """
    evaluated = []
    for route in state["available_routes"]:
        score = 100  # base score
        eta = route.get("eta_days")
        if isinstance(eta, int):
            score -= eta  
        else:
            score -= 50  
        evaluated.append({"route": route,"score": score})
    evaluated.sort(key=lambda r: r["score"], reverse=True)
    state["evaluated_routes"] = evaluated
    state["logs"].append(f"Evaluated {len(evaluated)} routes.")
    return state
def choose_best_route(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Step 4:
    Select the top-scoring route.
    """
    if not state["evaluated_routes"]:
        state["selected_route"] = {}
        state["routing_decision"] = "no_routes_available"
        state["logs"].append("No routes available to select.")
        return state
    best = state["evaluated_routes"][0]["route"]
    state["selected_route"] = best
    state["routing_decision"] = "route_selected"
    state["logs"].append(f"Selected best route: {best.get('route_id')}.")
    return state
def build_final_report(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Step 5:
    Produce a final structured summary.
    """
    state["final_report"] = {
        "incident_id": state["incident_id"],
        "disrupted_port": state["disrupted_port_id"],
        "selected_route": state["selected_route"],
        "warehouse_info": state["warehouse_db_context"],
        "total_routes_analyzed": len(state["evaluated_routes"]),
        "decision": state["routing_decision"],
        "logs": state["logs"],}
    state["logs"].append("Final report generated.")
    return state
def run_graph(initial_state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Runs the entire process in sequence.
    """
    state = initial_state
    state = load_warehouse_context(state)
    state = load_available_routes(state)
    state = evaluate_routes(state)
    state = choose_best_route(state)
    state = build_final_report(state)
    return state
if __name__ == "__main__":
    example_state: LogisticsIncidentState = {
        "incident_id": "INC-001",
        "manifest_text": "Sample manifest",
        "disrupted_port_id": "PORT-SEATTLE-02",
        "extracted_metadata": {"warehouse_id": "WH-WEST-202"},
        "routing_rag_context": "",
        "available_routes": [],
        "current_route_index": 0,
        "selected_route": {},
        "warehouse_db_context": {},
        "reroute_impact_score": 0,
        "routing_decision": "",
        "clarification_attempts": 0,
        "max_clarification_attempts": 2,
        "logs": [],
        "evaluated_routes": [],
        "final_report": {}
    }
    result = run_graph(example_state)
    print("FINAL REPORT:", result["final_report"])