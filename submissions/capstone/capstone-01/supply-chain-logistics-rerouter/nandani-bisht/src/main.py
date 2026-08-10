import os
import json
import sys
from dotenv import load_dotenv
from src.graph import app
from src.state import get_initial_state

load_dotenv()

def load_incidents():
    """Load the sample incidents from the data folder."""
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_incidents.json")
    if not os.path.exists(data_path):
        print(f"Error: Sample incidents file not found at {data_path}")
        sys.exit(1)
        
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_incident(incident):
    """Run the LangGraph workflow on a single incident."""
    print("\n" + "="*50)
    print(f"Running LangGraph workflow for incident: {incident['incident_id']}")
    print("="*50)

    initial_state = get_initial_state(
        incident_id=incident["incident_id"],
        manifest_text=incident["manifest_text"],
        disrupted_port_id=incident["disrupted_port_id"]
    )
    
    final_state = app.invoke(initial_state)
    
    print("\n Workflow Execution Logs ")
    for log in final_state.get("logs", []):
        print(log)
        
    report = final_state.get("final_report", {})
    decision = report.get("graph_routing_metadata", {}).get("final_decision_state", "UNKNOWN")
    loops = report.get("graph_routing_metadata", {}).get("loops_executed", 0)
    score = report.get("graph_routing_metadata", {}).get("reroute_impact_score", 0)
    
    print("\n" + "="*50)
    print("Workflow Execution Complete!")
    print(f"Final Decision: {decision}")
    print(f"Loops (Retries) Executed: {loops}")
    print(f"Reroute Impact Score: {score}")
    print("="*50)
    
    print("\n--- Final Advisory Report (Saved in outputs/) ---")
    print(json.dumps(report, indent=2))
    print("="*50 + "\n")
    return report

def main():
    incidents = load_incidents()
    
    print("Logistic Crisis Managment and Re-Router")
    print("Available Incidents:")
    for idx, inc in enumerate(incidents, 1):
        print(f"{idx}. {inc['incident_id']} - {inc['manifest_text'][:60]}...")
    print(f"{len(incidents) + 1}. Run All Incidents")
    
    choice_str = input(f"\nSelect incident (1-{len(incidents) + 1}): ").strip()
    
    try:
        choice = int(choice_str)
    except ValueError:
        print("Invalid input. Please enter a number.")
        sys.exit(1)
        
    if choice == len(incidents) + 1:
        print("Running all incidents")
        for inc in incidents:
            run_incident(inc)
    elif 1 <= choice <= len(incidents):
        run_incident(incidents[choice - 1])
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
