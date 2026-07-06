# state.py

# from typing import TypedDict
from typing_extensions import TypedDict

class LogisticsIncidentState(TypedDict):
    # Input
    incident_id: str
    manifest_text: str
    disrupted_port_id: str

    # LangChain output
    extracted_metadata: dict

    # RAG
    routing_rag_context: str

    # Routes
    available_routes: list
    current_route_index: int
    selected_route: dict

    # Warehouse
    warehouse_db_context: dict

    # Decision
    reroute_impact_score: int
    routing_decision: str

    # Retry Loop - logic
    clarification_attempts: int
    max_clarification_attempts: int

    # Logging 
    logs: list
    routes_evaluated: list

    # Final Output
    final_report: dict
