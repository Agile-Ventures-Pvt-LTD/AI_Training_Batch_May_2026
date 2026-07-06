import asyncio
import json
import os
from src.main import run_pipeline

async def main():
    print("Running automated incident execution script...")
    db_path = "data/sample_incidents.json"
    
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found.")
        return
        
    with open(db_path, "r", encoding="utf-8") as f:
        incidents = json.load(f)
        
    for inc in incidents:
        print(f"\nProcessing {inc['incident_id']}...")
        res = await run_pipeline(inc["incident_id"], inc["manifest_text"], inc["disrupted_port_id"])
        print(f"Incident {inc['incident_id']} complete. Decision: {res.get('routing_decision')}")

if __name__ == "__main__":
    asyncio.run(main())



### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026