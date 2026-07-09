from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from fastmcp import FastMCP
mcp = FastMCP("Service Health MCP Server")
DATA_FILE = Path("data/service_health.json")
def load_data() -> dict[str, Any]:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
@mcp.tool
def list_services() -> dict:
    """
    List all enterprise services  
    """
    data = load_data()
    services = [
        {"service_name": service["service_name"],"status": service["status"],
            "region": service["region"],}
        for service in data.get("services", [])]

    return {"count": len(services),"services": services,}
@mcp.tool
def get_service_health(service_name: str) -> dict:
    """
    Return detailed health  for a service
    """
    data = load_data()
    for service in data.get("services", []):
        if service["service_name"].lower() == service_name.lower():
            return {"found": True,"service": service,}
    return {"found": False,"message": "Service not found",}

@mcp.tool
def get_active_incidents(service_name: str | None = None,) -> dict:
    """
    Return active incidents
    """
    data = load_data()
    incidents = [ incident
        for incident in data.get("incidents", [])
        if incident.get("status") == "ACTIVE"
    ]

    if service_name:
        incidents = [incident
            for incident in incidents
            if incident["service_name"].lower()
            == service_name.lower()]

    return {"count": len(incidents),"incidents": incidents,}
if __name__ == "__main__":
    mcp.run()