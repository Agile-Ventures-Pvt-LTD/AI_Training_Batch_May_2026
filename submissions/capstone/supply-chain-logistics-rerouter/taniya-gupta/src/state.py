from typing import TypedDict, List, Dict

class LogisticsIncidentState(TypedDict):
    incident_id: str
    manifest_text: str
    disrupted_port_id: str
    extracted_metadata: Dict
    routing_rag_context: str
    available_routes: List
    current_route_index: int
    selected_route: Dict
    warehouse_db_context: Dict
    reroute_impact_score: int
    routing_decision: str
    clarification_attempts: int
    max_clarification_attempts: int
    logs: List[str]
    final_report: Dict
    routes_evaluated: List
    loops_executed: int

