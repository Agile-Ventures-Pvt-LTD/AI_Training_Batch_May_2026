from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from fastmcp import FastMCP
mcp = FastMCP("Change Management MCP Server")
DATA_FILE = Path("data/changes.json")
def load_changes() -> list[dict[str, Any]]:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    if isinstance(data, list):
        return data
    return data.get("changes", [])
@mcp.tool
def list_recent_changes(limit: int = 10,)-> dict:
    """
    Return most recent change records.
    """
    changes = sorted(load_changes(),key=lambda x: x.get("implemented_at", ""),reverse=True,)
    results = changes[:limit]
    return {"count": len(results),"changes": results,}

@mcp.tool
def get_change_details(change_id: str,) -> dict:
    """
    Return details for a specific change.
    """
    for change in load_changes():
        if change["change_id"] == change_id:
            return {"found": True,"change": change,}
    return {"found": False,"message": "Change not found.",}
@mcp.tool
def get_changes_for_service(service_name: str,) -> dict:
    """
    Return recent change
    """
    changes = [change for change in load_changes() if change["service_name"].lower()== service_name.lower()]
    changes.sort(key=lambda x: x.get("implemented_at", ""),reverse=True,)
    return {"service_name": service_name,"count": len(changes),"changes": changes,}


if __name__ == "__main__":
    mcp.run()