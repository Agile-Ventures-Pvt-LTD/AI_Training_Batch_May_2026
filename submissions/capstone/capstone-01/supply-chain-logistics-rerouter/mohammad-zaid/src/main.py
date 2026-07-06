
import json
from pathlib import Path
import sys
from graph import app
from rag import create_vector_db
from report_writer import save_report
sys.path.insert(0, str(Path(__file__).parent.parent))

# create_vector_db()  - uncomment if running for the first time

# Load incidents

with open(Path("data") / "sample_incidents.json", "r", encoding="utf-8") as f:
    incidents = json.load(f)

print("\nAvailable Incidents: \n") # -> list from sample_incidents.json

for i, incident in enumerate(incidents, start=1):
    print(f"{i}. {incident['incident_id']}")

choice = int(input("\nSelect Incident : ")) - 1

incident = incidents[choice]


# Initial Graph State

initial_state = {
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
    "max_clarification_attempts": 2,

    "logs": [],
    "routes_evaluated": [],

    "final_report": {},
}


# Execute the Graph

final_state = app.invoke(
    input = initial_state
    ) 
print(f"Final State of Graph:\n {final_state}")

# Save the Report
save_report(final_state)
print(f"\nDecision : {final_state['routing_decision']}")
print(f"Report Saved : outputs/{incident['incident_id']}_reroute_advisory_report.json")
