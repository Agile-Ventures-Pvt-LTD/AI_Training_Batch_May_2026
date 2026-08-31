from pathlib import Path
from fastmcp import FastMCP
import json

mcp = FastMCP("Change Management MCP Server")

DATA_FILE = Path(__file__).parent.parent / "data" / "changes.json"

def load_data():
    with open(DATA_FILE,"r") as f:
        return json.load(f)
    
@mcp.tool
def list_recent_changes(limit:int=10) -> dict:
    """Return recent changes records."""
    data = load_data()
    changes = sorted(data["changes"],key = lambda x: x["implemented_at"],reverse=True)
    safe_limit = min(max(limit,1),50)
    limited_changes = [
        {
            "change_id": c["change_id"],
            "service_name": c["service_name"],
            "change_type": c["change_type"],
            "status": c["status"],
            "risk": c["risk"],
            "implemented_at": c["implemented_at"]
        } for c in changes[:safe_limit]
    ]
    return {"count":len(limited_changes),"changes":limited_changes}

@mcp.tool
def get_change_details(change_id:str) -> dict:
    """Return details of a specific change."""
    data = load_data()
    for c in data["changes"]:
        if c["change_id"].lower() == change_id.lower():
            return {"found":True,"change":c}
    return {"found":False, "message":"Change not found."}

@mcp.tool
def get_changes_for_service(service_name:str) -> dict:
    """Find recent changes for a service."""
    data = load_data()
    filtered = [c for c in data["changes"] if c["service_name"].lower() == service_name.lower()]
    mapped_changes = [
        {
            "change_id": c["change_id"],
            "change_type": c["change_type"],
            "risk": c["risk"],
            "implemented_at": c["implemented_at"],
            "summary": c["summary"],
            "rollback_available": c["rollback_available"]
        } for c in filtered
    ]
    return {"service_name": service_name,"count": len(mapped_changes),"changes": mapped_changes}

if __name__ == "__main__":
    mcp.run()