import json
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("Service Health MCP Server")

def load_data() -> dict:
    data_path = Path(__file__).resolve().parents[1] / "data" / "service_health.json"
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"services": [], "incidents": []}

@mcp.tool
def list_services() -> dict:
    """List enterprise services and current health status.
    
    Returns:
        A dictionary containing count and list of services with service_name, status, and region.
    """
    data = load_data()
    services_list = []
    for s in data.get("services", []):
        services_list.append({
            "service_name": s.get("service_name"),
            "status": s.get("status"),
            "region": s.get("region")
        })
    return {
        "count": len(services_list),
        "services": services_list
    }

@mcp.tool
def get_service_health(service_name: str) -> dict:
    """Return detailed health information for one service.
    
    Args:
        service_name: The name of the service to inspect.
        
    Returns:
        Detailed metrics of the service if found, or a failure message.
    """
    data = load_data()
    for s in data.get("services", []):
        if s.get("service_name") == service_name:
            return {
                "found": True,
                "service": s
            }
    return {
        "found": False,
        "message": "Service not found."
    }

@mcp.tool
def get_active_incidents(service_name: str | None = None) -> dict:
    """Return active operational incidents. The tool may optionally filter by service.
    
    Args:
        service_name: Optional name of the service to filter incidents by.
        
    Returns:
        A dictionary containing count and list of active incidents.
    """
    data = load_data()
    active_incidents = []
    for inc in data.get("incidents", []):
        if inc.get("status") == "ACTIVE":
            if service_name is None or inc.get("service_name") == service_name:
                active_incidents.append(inc)
                
    return {
        "count": len(active_incidents),
        "incidents": active_incidents
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
