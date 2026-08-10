import json
import sys
from fastmcp import FastMCP
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import CHANGES_FILE

cms_mcp = FastMCP("Change Management MCP Server")


def _load_changes() -> list:
    if not CHANGES_FILE.exists():
        return []
    with open(CHANGES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else data.get("changes", [])


@cms_mcp.tool
def list_recent_changes(limit: int = 10) -> dict:
    """Returns recent change records ordered by implementation date."""
    changes = _load_changes()
    sorted_changes = sorted(
        changes, key=lambda x: x.get("implemented_at", ""), reverse=True
    )
    sliced = sorted_changes[:limit]

    summary = [
        {
            "change_id": c.get("change_id"),
            "service_name": c.get("service_name"),
            "change_type": c.get("change_type"),
            "status": c.get("status"),
            "risk": c.get("risk"),
            "implemented_at": c.get("implemented_at"),
        }
        for c in sliced
    ]
    return {"count": len(summary), "changes": summary}


@cms_mcp.tool
def get_change_details(change_id: str) -> dict:
    """Returns details of a specific change."""
    changes = _load_changes()
    for c in changes:
        if c.get("change_id", "").lower() == change_id.lower():
            return {"found": True, "change": c}
    return {"found": False, "message": "Change not found."}


@cms_mcp.tool
def get_changes_for_service(service_name: str) -> dict:
    """Find recent changes for a service."""
    changes = _load_changes()
    matched = [
        c for c in changes if c.get("service_name", "").lower() == service_name.lower()
    ]

    summary = [
        {
            "change_id": c.get("change_id"),
            "change_type": c.get("change_type"),
            "risk": c.get("risk"),
            "implemented_at": c.get("implemented_at"),
            "summary": c.get("summary"),
            "rollback_available": c.get("rollback_available", False),
        }
        for c in matched
    ]
    
    rollback_any = any(c.get("rollback_available", False) for c in matched)
    
    return {
        "service_name": service_name,
        "count": len(summary),
        "changes": summary,
        "rollback_available": rollback_any
    }


if __name__ == "__main__":
    cms_mcp.run()