import json
import os
from dotenv import load_dotenv
from graph import app

load_dotenv()

os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
incidents_path = "data/sample_incidents.json"

with open(incidents_path, "r") as f:
        incidents = json.load(f)

print("Available Incidents:")

try:
        selection = input(f"Select incident (1-3): ")
        if not selection.isdigit():
            print("Invalid input. Please enter a number.")
            
        idx = int(selection) - 1
        if idx < 0 or idx >= len(incidents):
            print("Selection out of range.")
          
        selected_inc = incidents[idx]
        
        initial_input = {
            "incident_id": selected_inc["incident_id"],
            "manifest_text": selected_inc["manifest_text"],
            "disrupted_port_id": selected_inc["disrupted_port_id"],
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
            "routes_evaluated": [],
            "loops_executed": 0
        }

        final_state = app.invoke(initial_input)
        
        report = final_state.get("final_report")
        decision_state = report.get("graph_routing_metadata").get("final_decision_state")
        
        print(f"Incident ID:    {report.get('incident_id')}")
        print(f"Final Decision: {decision_state}")
        print(f"Brief summary:  {report.get('original_incident_summary')}")
        print(f"Operations Brief:\n{report.get('final_operations_brief')}")
        print(f"Report saved to outputs/{selected_inc['incident_id']}_reroute_advisory_report.json")
        print(f"Latest report saved to outputs/reroute_advisory_report.json")
        
except KeyboardInterrupt:
        print("\nOperation cancelled.")
except Exception as e:
        print(f"\nAn error occurred during execution: {e}")
