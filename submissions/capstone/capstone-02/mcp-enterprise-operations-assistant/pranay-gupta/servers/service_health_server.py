import json
from fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("Service Health MCP Server")

DATA_FILE = Path(__file__).parent.parent / "data" / "service_health.json"

def load_data():
    with open(DATA_FILE,"r") as f:
        return json.load(f)
    
@mcp.tool
def list_services() -> dict:
    """List enterprise services and current health status."""
    data = load_data()
    services = [
        {
            "service_name": s["service_name"],
            "status": s["status"],
            "region": s["region"]
        } for s in data["services"]
    ]
    return {"count":len(services),"services": services}

@mcp.tool
def get_service_health(service_name:str) -> dict:
    """Return detailed health information for a service."""
    data = load_data()
    for s in data["services"]:
        if s["service_name"].lower() == service_name.lower():
            return {"found": True,"service":s}
    return {"found": False,"message":"service not found."}

@mcp.tool
def get_active_incidents(service_name:str) -> dict:
    """Return active operational incidents."""
    data = load_data()
    incident = data["active_incident_ids"]
    if service_name:
        filtered = [i for i in incident if i["service_name"].lower() == service_name.lower()]
        return {"count":len(filtered),"incidents":filtered}
    return {"count":len(incident),"incidents":incident}

if __name__ == "__main__":
    mcp.run()


