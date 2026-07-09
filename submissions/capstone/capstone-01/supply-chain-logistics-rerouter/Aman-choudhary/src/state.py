from typing import Any, TypedDict
class LogisticsIncidentState(TypedDict):
    """
    Shared LangGraph State
    """
    incident_id: str
    manifest_text: str
    disrupted_port_id: str
    extracted_metadata: dict[str, Any]
    routing_rag_context: str
    available_routes: list[dict[str, Any]]
    current_route_index: int
    selected_route: dict[str, Any]
    warehouse_db_context: dict[str, Any]
    reroute_impact_score: int
    routing_decision: str
    clarification_attempts: int
    max_clarification_attempts: int
    logs: list[str]
    evaluated_routes: list[dict[str, Any]]
    final_report: dict[str, Any]