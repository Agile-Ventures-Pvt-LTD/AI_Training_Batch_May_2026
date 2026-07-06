import os
import json
from dotenv import load_dotenv

load_dotenv()

from src.graph import app

def run_workflow():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "sample_incidents.json"))
    
    if not os.path.exists(data_path):
        print("Missing")
        return
        
    with open(data_path, "r", encoding="utf-8") as f:
        incidents = json.load(f)
        
    print("Supply Chain Crisis Management and Logistics Re-Router")

      
    try:
        selection = int(input("Select an incident to evaluate from 1 to 3: \n Available Incidents:1. INC-001 \n 2. INC-002 \n 3. INC-003 \n Select incident: ")) - 1
        if selection not in range(len(incidents)):
            print("Please select valid input")
            return
    except ValueError:
        print("Enter valid input number")
        return
        
    selected = incidents[selection]
 
    initial_state = {"incident_id": selected["incident_id"],"manifest_text": selected["manifest_text"],"disrupted_port_id": selected["disrupted_port_id"],"extracted_metadata": {},"routing_rag_context": "","available_routes": [],"current_route_index": 0,"selected_route": None,"warehouse_db_context": None,"reroute_impact_score": 0,"routing_decision": "","clarification_attempts": 0,"max_clarification_attempts": 2,"logs": [],"final_report": None}
    
    final_state = app.invoke(initial_state)
    
    output_name = f"{selected['incident_id']}_reroute_advisory_report.json"
    target_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", output_name))
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(final_state["final_report"], f, indent=2)

    print("Output is saved.")
        
if __name__ == "__main__":
    run_workflow()
