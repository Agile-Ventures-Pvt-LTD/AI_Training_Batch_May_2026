from typing import TypedDict

class LogisticsIncidentState(TypedDict):
    """Represents the state of our query routing workflow"""
    incident_id: str
    manifest_text: str
    disrupted_port_id: str
    extracted_metadata: dict
    routing_rag_context: str
    available_routes: list
    current_route_index: int
    selected_route: dict
    warehouse_db_context: dict
    reroute_impact_score: int
    routing_decision: str
    clarification_attempts: int
    max_clarification_attempts: int
    final_report: dict
    final_state:str
    final_operations_brief:dict
    logs:list
