from typing import Required, TypedDict
from typing import List
from typing import Dict
from typing import Optional

class LogisticsIncidentState(TypedDict):
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

    logs: list[str]
    
    final_report: dict

