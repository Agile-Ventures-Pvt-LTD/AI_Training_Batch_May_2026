import json
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("Change Management MCP Server")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "changes.json"

def _load_data():
    with open(DATA_PATH) as f:
        return json.load(f)

@mcp.tool
def list_recent_changes(limit: int = 10) -> dict:
    """Return recent change records, most recent first."""
    data = _load_data()
    changes = sorted(data["changes"], key=lambda c: c["implemented_at"], reverse=True)
    changes = changes[:limit]
    result = [
        {
            "change_id": c["change_id"],
            "service_name": c["service_name"],
            "change_type": c["change_type"],
            "status": c["status"],
            "risk": c["risk"],
            "implemented_at": c["implemented_at"],
        }
        for c in changes
    ]
    return {"count": len(result), "changes": result}

@mcp.tool
def get_change_details(change_id: str) -> dict:
    """Return details of a specific change by change ID."""
    data = _load_data()
    for c in data["changes"]:
        if c["change_id"] == change_id:
            return {"found": True, "change": c}
    return {"found": False, "message": "Change not found."}

@mcp.tool
def get_changes_for_service(service_name: str) -> dict:
    """Find recent changes for a specific service by name."""
    data = _load_data()
    changes = [
        {
            "change_id": c["change_id"],
            "change_type": c["change_type"],
            "risk": c["risk"],
            "implemented_at": c["implemented_at"],
            "summary": c["summary"],
            "rollback_available": c["rollback_available"],
        }
        for c in data["changes"]
        if c["service_name"].lower() == service_name.lower()
    ]
    return {"service_name": service_name, "count": len(changes), "changes": changes}

if __name__ == "__main__":
    mcp.run()