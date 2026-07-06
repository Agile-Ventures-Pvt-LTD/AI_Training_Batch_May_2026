import asyncio
import json
import os
from src.graph import supply_app

async def run_pipeline(incident_id: str, manifest: str, port_id: str) -> dict:
    """Helper function to run the full supply chain rerouting pipeline."""
    initial_input = {
        "incident_id": incident_id,
        "manifest_text": manifest,
        "disrupted_port_id": port_id,
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
        "final_report": {}
    }
    return await supply_app.ainvoke(initial_input)

async def main():
    print("==================================================")
    print("SUPPLY CHAIN CRISIS & LOGISTICS RE-ROUTER")
    print("==================================================")
    print("1. Process Sample Incident INC-001")
    print("2. Process Sample Incident INC-002")
    print("3. Process Sample Incident INC-003")
    print("4. Custom Incident Chatbot Mode")
    print("5. Exit")
    print("==================================================")
    
    # Load sample incidents
    db_path = "data/sample_incident.json"
    sample_incidents = []
    if os.path.exists(db_path):
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                sample_incidents = json.load(f)
        except Exception as e:
            print(f"Error loading sample incidents: {e}")

    while True:
        try:
            choice = input("\nSelect Option > ").strip()
            if choice == "5" or choice.lower() in ["exit", "quit"]:
                print("Exiting. Goodbye!")
                break
                
            if choice in ["1", "2", "3"]:
                idx = int(choice) - 1
                if idx < len(sample_incidents):
                    inc = sample_incidents[idx]
                    print(f"\nProcessing {inc['incident_id']}...")
                    res = await run_pipeline(inc["incident_id"], inc["manifest_text"], inc["disrupted_port_id"])
                    
                    print("\n=== Execution Summary ===")
                    print(f"Incident ID:         {res.get('incident_id')}")
                    print(f"Final Decision:      {res.get('routing_decision')}")
                    print(f"Loops Executed:      {res.get('current_route_index', 0)}")
                    print(f"Impact Score:        {res.get('reroute_impact_score', 0)}")
                    if res.get('routing_decision') == 'OPTIMAL_PATH_FOUND':
                        print(f"Final Selected Route: {res.get('selected_route', {}).get('route_id')}")
                        print(f"Assigned Warehouse:   {res.get('selected_route', {}).get('warehouse_id')}")
                    else:
                        print("Result:              ESCALATED TO REGIONAL OPERATIONS DIRECTOR")
                    print("\n--- Final Operations Brief ---")
                    print(res.get("final_report", {}).get("final_operations_brief", "No brief generated."))
                else:
                    print(f"Sample incident indexing failed. Total loaded: {len(sample_incidents)}")
            elif choice == "4":
                print("\n--- Custom Incident Chatbot Mode ---")
                print("Enter your shipping disruption query (e.g. stranded vessel, cargo type, etc.).")
                print("Type 'back' to return to main menu.")
                while True:
                    manifest = input("\nIncident Manifest > ").strip()
                    if manifest.lower() == "back":
                        break
                    if not manifest:
                        continue
                    port = input("Disrupted Port ID [default: PORT-SEATTLE-02] > ").strip()
                    if not port:
                        port = "PORT-SEATTLE-02"
                        
                    res = await run_pipeline("INC-CUSTOM", manifest, port)
                    
                    print("\n=== Advisory Report ===")
                    print(f"Decision Status: {res.get('routing_decision')}")
                    print(f"Impact Score:    {res.get('reroute_impact_score')}")
                    print(f"Brief:           {res.get('final_report', {}).get('final_operations_brief')}")
            else:
                print("Invalid option. Please choose 1-5.")
        except KeyboardInterrupt:
            print("\nReturning to menu...")
        except Exception as e:
            print(f"Runtime error: {e}")

if __name__ == "__main__":
    asyncio.run(main())


### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026