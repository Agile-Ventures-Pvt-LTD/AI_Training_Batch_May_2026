import os
import json
import sys
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv
load_dotenv()

from src.graph import agent_app
from src.state import LogisticsIncidentState

def load_incidents()->list[Dict]:
    incidents_path = Path("data/sample_incidents.json")
    if not incidents_path.is_file():
        raise FileNotFoundError("Mising the incidents file")
    with incidents_path.open("r",encoding="utf-8") as f:
        return json.load(f)
    
def pick_incident(incidents: list[Dict]) -> Dict:
    print("Available Shipping Incidents")
    for i, inc in enumerate(incidents, start=1):
        print(f"{i}. {inc.get('incident_id', 'UNKNOWN')} - {inc.get('summary', '')}")
    if len(sys.argv) > 1:
        try:
            choice = int(sys.argv[1])
            if 1 <= choice <= len(incidents):
                return incidents[choice - 1]
        except ValueError:
            pass

    while True:
        try:
            choice = int(input("\nSelect an incident by number: ").strip())
            if 1 <= choice <= len(incidents):
                return incidents[choice - 1]
            else:
                print(" Number out of range.")
        except ValueError:
            print(" Invalid input - please enter a number.")
            
def build_initial_state(incident: Dict) -> LogisticsIncidentState:
    return {
        "incident_id": incident["incident_id"],
        "manifest_text": incident["manifest_text"],
        "disrupted_port_id": incident["disrupted_port_id"],
        "extracted_metadata": {},          
        "routing_rag_context": "",         
        "available_routes": [],            
        "current_route_index": 0,
        "selected_route": {},
        "warehouse_db_context": {},
        "reroute_impact_score": 0,
        "routing_decision": "",
        "clarification_attempts": 0,
        "max_clarification_attempts": 0,
        "logs": [],
        "final_report": {}
    }  


def run_workflow(initial_state: LogisticsIncidentState) -> LogisticsIncidentState:
    result = agent_app.invoke(initial_state)
    return result

def main() -> None:
    load_dotenv()                     
    incidents = load_incidents()
    incident = pick_incident(incidents)

    print(f"\n Processing incident {incident['incident_id']} ...")
    state = build_initial_state(incident)

    final_state = run_workflow(state)

    report_path = Path("outputs") / f"{incident['incident_id']}_reroute_advisory_report.json"
    print(f"\n Advisory report generated: {report_path.resolve()}")
    print("\n--- Graph Logs ---")
    for entry in final_state.get("logs", []):
        print(f"* {entry}")


if __name__ == "__main__":
    main()