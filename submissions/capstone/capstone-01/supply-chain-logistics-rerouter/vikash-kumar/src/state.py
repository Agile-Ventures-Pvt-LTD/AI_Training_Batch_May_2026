from typing import TypedDict, List, Optional

class LogisticsIncidentState(TypedDict):
    incident_id: str
    manifest_text: str
    disrupted_port_id: str
    
    extracted_metadata: dict
    routing_rag_context: str
    available_routes: list
    current_route_index: int
    selected_route: Optional[dict]
    warehouse_db_context: Optional[dict]
    
    reroute_impact_score: int
    routing_decision: str  
    clarification_attempts: int
    max_clarification_attempts: int
    logs: List[str]
    final_report: Optional[dict]
