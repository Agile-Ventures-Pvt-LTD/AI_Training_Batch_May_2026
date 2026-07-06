from src.config import SAMPLE_INCIDENT_PATH, ensure_output_dir
from src.graph import build_workflow

import json
import sys

def load_sample_incidents():
    with open(SAMPLE_INCIDENT_PATH,"r",encoding="utf-8") as data:
        return json.load(data)
    
def display_incidents(incidents):
    print("Available Incidents:")
    for idx,incident in enumerate(incidents,start=1):
        print(f"{idx}. {incident['incident_id']}")
    print("\n\n")

def run_incident(incident:dict,app):
    print(f"Processing {incident['incident_id']}...")
    print(f"Manifest: {incident['manifest_text'][:100]}...")

    initial_input={
        "incident_id": incident["incident_id"],
        "manifest_text": incident["manifest_text"],
        "disrupted_port_id": incident["disrupted_port_id"],
    }

    final_state = app.invoke(initial_input)

    report = final_state.get("final_report",{})
    routing_meta = report.get("graph_routing_metadata",{})

    print(f"incident: {incident['incident_id']}")
    print(f"final Decision: {routing_meta.get('final_decision_state','N/A')}")
    print(f"Route Evaluated: {len(report.get('routes_evaluated',[]))}")
    print(f"Loops Executed: {routing_meta.get('loop_executed',0)}")
    print(f"Reroute Impact Score: {routing_meta.get('reroute_impact_score',0)}")

    final_route = report.get("final_selected_route",{})
    if final_route:
        print(f"Selected Route: {final_route.get('route_id','N/A')}")
    print(f"Operations Brief:")
    print(report.get("final_operations_brief","N/A"))
    print("\n\n")

    return final_state

def main():
    ensure_output_dir()

    incidents = load_sample_incidents()

    if len(sys.argv) > 1:
        selection = sys.argv[1]
    else:
        display_incidents(incidents)
        selection = input("Select incident (1-3, or 'all'): ").strip()

    app = build_workflow()

    if selection.lower() == "all":
        for incident in incidents:
            run_incident(incident, app)
    else:
        try:
            idx = int(selection) - 1
            if 0 <= idx < len(incidents):
                run_incident(incidents[idx], app)
            else:
                print(f"Invalid selection: {selection}")
        except ValueError:
            print(f"Invalid input: {selection}")

    return

if __name__ == "__main__":
    main()