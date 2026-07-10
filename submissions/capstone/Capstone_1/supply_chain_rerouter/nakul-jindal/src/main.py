import json
from src.graph import build_graph
from src.report_writer import save_report

def load_incidents():
    with open("data/sample_incidents.json") as f:
        return json.load(f)

def run_incident(incident: dict, app):
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
        "evaluated_routes": [],
        "logs": [],
        "final_report": {},
    }
    final_state = app.invoke(initial_state)
    path = save_report(final_state["final_report"], incident["incident_id"])
    print(f"Saved: {path}")

if __name__ == "__main__":
    incidents = load_incidents()
    app = build_graph()

    print("Available Incidents:")
    for i, inc in enumerate(incidents, 1):
        print(f"{i}. {inc['incident_id']}")

    choice = input("Select incident (or 'all'): ").strip()
    if choice.lower() == "all":
        for inc in incidents:
            run_incident(inc, app)
    else:
        run_incident(incidents[int(choice) - 1], app)
