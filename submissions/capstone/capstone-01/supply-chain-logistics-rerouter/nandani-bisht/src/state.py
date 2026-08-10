from typing import TypedDict, List, Dict, Any, Optional

class LogisticsIncidentState(TypedDict):
    incident_id: str
    manifest_text: str
    disrupted_port_id: str
    original_incident_summary: str
    extracted_metadata: Dict[str, Any]
    routing_rag_context: str
    rag_validation_rules_applied: List[str]
    available_routes: List[Dict[str, Any]]
    current_route_index: int
    selected_route: Dict[str, Any]
    warehouse_db_context: Dict[str, Any]
    reroute_impact_score: int
    routing_decision: str 
    routes_evaluated: List[Dict[str, Any]]
    clarification_attempts: int
    max_clarification_attempts: int
    logs: List[str]
    final_report: Dict[str, Any]
    

def get_initial_state(incident_id: str, manifest_text: str, disrupted_port_id: str) -> LogisticsIncidentState:
    """Return the initial state dictionary for a shipping incident."""
    return {
        "incident_id": incident_id,
        "manifest_text": manifest_text,
        "disrupted_port_id": disrupted_port_id,
        "original_incident_summary": "",
        "extracted_metadata": {},
        "routing_rag_context": "",
        "rag_validation_rules_applied": [],
        "available_routes": [],
        "current_route_index": 0,
        "selected_route": {},
        "warehouse_db_context": {},
        "reroute_impact_score": 0,
        "routing_decision": "",
        "routes_evaluated": [],
        "clarification_attempts": 0,
        "max_clarification_attempts": 2,
        "logs": [],
        "final_report": {}
    }
