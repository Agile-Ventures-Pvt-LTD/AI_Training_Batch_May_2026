# service-health
# ├── list_services
# ├── get_service_health
# └── get_active_incidents
# support-ticket
# ├── search_tickets
# ├── get_ticket_details
# └── get_high_priority_tickets
# change-management
# ├── list_recent_changes
# ├── get_change_details
# └── get_changes_for_service


import json
from pathlib import Path
from mcp_use import MCPClient
from src.config import config
import asyncio

async def run_tool_discovery():
    "Connect all mcp servers"
    client=MCPClient(config)
    discovered={}
    try:
        await client.create_all_sessions()
        for server_name in client.get_server_names():
            sessions= client.get_session(server_name)
            tools=await sessions.list_tools()
            discovered[server_name]= [t.name for t in tools]
    finally:
        await client.close_all_sessions()

    out_dir= Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True, parents=True)
    output_file=out_dir / "tool_discovery.json"

    with open(output_file, "w") as f:
        json.dump(discovered,f, indent=2)
    
    print("Discovered tools are saved")
    return discovered

if __name__=="__main__":
    asyncio.run(run_tool_discovery())