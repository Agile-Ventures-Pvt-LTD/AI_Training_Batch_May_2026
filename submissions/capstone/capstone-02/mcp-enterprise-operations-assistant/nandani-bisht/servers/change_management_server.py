import json
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("Change Management MCP Server")

def load_data() -> dict:
    data_path = Path(__file__).resolve().parents[1] / "data" / "changes.json"
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"changes": []}

@mcp.tool
def list_recent_changes(limit: int = 10) -> dict:
    """Return recent change records sorted by implementation date descending.
    
    Args:
        limit: The maximum number of changes to return (default 10).
        
    Returns:
        A dictionary containing count and list of recent changes.
    """
    data = load_data()
    changes = data.get("changes", [])
    
    sorted_changes = sorted(changes, key=lambda c: c.get("implemented_at", ""), reverse=True)
    
    formatted_changes = []
    for c in sorted_changes[:limit]:
        formatted_changes.append({
            "change_id": c.get("change_id"),
            "service_name": c.get("service_name"),
            "change_type": c.get("change_type"),
            "status": c.get("status"),
            "risk": c.get("risk"),
            "implemented_at": c.get("implemented_at")
        })
        
    return {
        "count": len(formatted_changes),
        "changes": formatted_changes
    }

@mcp.tool
def get_change_details(change_id: str) -> dict:
    """Return details of a specific change.
    
    Args:
        change_id: The unique identifier of the change (e.g., CHG-2001).
        
    Returns:
        Detailed change information if found, or a failure message.
    """
    data = load_data()
    for c in data.get("changes", []):
        if c.get("change_id") == change_id:
            return {
                "found": True,
                "change": c
            }
    return {
        "found": False,
        "message": "Change not found."
    }

@mcp.tool
def get_changes_for_service(service_name: str) -> dict:
    """Find recent changes for a service.
    
    Args:
        service_name: The name of the service to query.
        
    Returns:
        A dictionary containing service name, count, and list of changes.
    """
    data = load_data()
    changes = []
    for c in data.get("changes", []):
        if c.get("service_name") == service_name:
            changes.append({
                "change_id": c.get("change_id"),
                "change_type": c.get("change_type"),
                "risk": c.get("risk"),
                "implemented_at": c.get("implemented_at"),
                "summary": c.get("summary"),
                "rollback_available": c.get("rollback_available")
            })
            
    sorted_changes = sorted(changes, key=lambda c: c.get("implemented_at", ""), reverse=True)
    
    return {
        "service_name": service_name,
        "count": len(sorted_changes),
        "changes": sorted_changes
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
