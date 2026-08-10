import json
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("Service Health MCP Server")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "service_health.json"

def _load_data():
    with open(DATA_PATH) as f:
        return json.load(f)

@mcp.tool
def list_services() -> dict:
    """List all enterprise services and their current health status."""
    data = _load_data()
    services = [
        {"service_name": s["service_name"], "status": s["status"], "region": s["region"]}
        for s in data["services"]
    ]
    return {"count": len(services), "services": services}

@mcp.tool
def get_service_health(service_name: str) -> dict:
    """Return detailed health information for a specific service by name."""
    data = _load_data()
    for s in data["services"]:
        if s["service_name"].lower() == service_name.lower():
            return {"found": True, "service": s}
    return {"found": False, "message": "Service not found."}

@mcp.tool
def get_active_incidents(service_name: str = None) -> dict:
    """Return active operational incidents, optionally filtered by service name."""
    data = _load_data()
    incidents = [inc for inc in data["incidents"] if inc["status"] == "ACTIVE"]
    if service_name:
        incidents = [inc for inc in incidents if inc["service_name"].lower() == service_name.lower()]
    return {"count": len(incidents), "incidents": incidents}

if __name__ == "__main__":
    mcp.run()