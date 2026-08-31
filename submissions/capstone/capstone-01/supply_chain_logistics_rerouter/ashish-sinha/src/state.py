from typing import TypedDict
from config import GROQ_MODEL
from config import GROQ_API_KEY

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

def create_initial_state(
    incident_id:str,
    manifest_text:str,
    disrupted_port_id:str) -> LogisticsIncidentState:
    return{
    "incident_id": incident_id,
    "manifest_text": manifest_text,
    "disrupted_port_id": disrupted_port_id,
    "extracted_metadata": {},
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
    "final_report": {},
    "routes_evaluated":[],
    "retieved_rules":[]
    }




