import os
import sys
import json
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from servers.service_health_server import mcp as health_mcp
from servers.support_ticket_server import mcp as ticket_mcp
from servers.change_management_server import mcp as change_mcp
from src.config import Mcp

async def export_tool():
    os.makedirs(Mcp.OUTPUTS_DIR, exist_ok=True)
    health_tools = await health_mcp.list_tools()
    ticket_tools = await ticket_mcp.list_tools()
    change_tools = await change_mcp.list_tools()
    
    registry = {"service-health": [t.name for t in health_tools],"support-ticket": [t.name for t in ticket_tools],"change-management": [t.name for t in change_tools]}
    
    output_path = os.path.join(Mcp.OUTPUTS_DIR, "tool_discovery.json")
    with open(output_path, "w") as f:
        json.dump(registry, f, indent=2)
    return registry

if __name__ == "__main__":
    asyncio.run(export_tool())
    print("Successfully! Saved at outputs/tool_discovery.json!")
