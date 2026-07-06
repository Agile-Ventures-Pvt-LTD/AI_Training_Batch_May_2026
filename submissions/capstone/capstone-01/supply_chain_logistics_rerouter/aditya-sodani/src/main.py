import json
from graph import build_graph
from report_writer import save_report

def main():

    with open("data/sample_incidents.json") as f:
        incidents = json.load(f)

    print("\nAvailable Incidents\n")

    for i,item in enumerate(incidents):
        print(i+1,item["incident_id"])

    choice = int(input("\nSelect Incident: "))

    incident = incidents[
        choice-1
    ]

    initial_state = {
        **incident,
        "extracted_metadata":{},
        "routing_rag_context":"",
        "available_routes":[],
        "current_route_index":0,
        "selected_route":{},
        "warehouse_db_context":{},
        "reroute_impact_score":0,
        "routing_decision":"",
        "clarification_attempts":0,
        "max_clarification_attempts":2,
        "routes_evaluated":[],
        "logs":[],
        "final_report":{}
    }

    app = build_graph()

    final_state = app.invoke(initial_state)

    path = save_report(
        incident["incident_id"],
        final_state["final_report"]
    )

    print("\nReport saved:",path)


if __name__ == "__main__":
    main()
 