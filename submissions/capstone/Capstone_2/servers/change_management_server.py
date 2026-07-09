## Change Management MCP Server
## Data source: data/changes.json

from __future__ import annotations
import os
import json
from typing import Any, Optional, Dict, List
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

class ChangeManagementError(RuntimeError):
    """Raised when change management data cannot be read or is malformed."""

mcp = FastMCP(name="change-management")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "changes.json")


def _load_data() -> List[Dict[str, Any]]:
    """
    Load the change management dataset from disk.

    Returns:
        A list of change records.

    Raises:
        ChangeManagementError if the file is missing or malformed.
    """
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise ChangeManagementError(f"Data file not found at {DATA_PATH}")
    except json.JSONDecodeError as e:
        raise ChangeManagementError(f"Malformed change data: {e}")

    # Support either a bare list or {"changes": [...]}
    if isinstance(data, dict) and "changes" in data:
        data = data["changes"]

    if not isinstance(data, list):
        raise ChangeManagementError("Unexpected change management data shape.")

    return data


def _sorted_by_recency(changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        changes,
        key=lambda c: c.get("implemented_at", ""),
        reverse=True,
    )


@mcp.tool
def list_recent_changes(limit: int = 10) -> Dict[str, Any]:
    """
    Return recent change records, most recent first.

    Args:
        limit: Maximum number of changes to return.

    Returns:
        A dict with "count" and "changes", each including change_id,
        service_name, change_type, status, risk, and implemented_at.
    """
    changes = _sorted_by_recency(_load_data())
    changes = changes[:limit]

    summarized = [
        {
            "change_id": c.get("change_id", ""),
            "service_name": c.get("service_name", ""),
            "change_type": c.get("change_type", ""),
            "status": c.get("status", ""),
            "risk": c.get("risk", ""),
            "implemented_at": c.get("implemented_at", ""),
        }
        for c in changes
    ]

    return {
        "count": len(summarized),
        "changes": summarized,
    }


@mcp.tool
def get_change_details(change_id: str) -> Dict[str, Any]:
    """
    Return details of a specific change.

    Args:
        change_id: The unique change identifier (e.g. "CHG-2001").

    Returns:
        A dict with "found" and, if found, the full "change" record
        including implemented_by, summary, and rollback_available.
    """
    changes = _load_data()

    for c in changes:
        if str(c.get("change_id", "")).lower() == change_id.lower():
            return {
                "found": True,
                "change": c,
            }

    return {
        "found": False,
        "message": "Change not found.",
    }


@mcp.tool
def get_changes_for_service(service_name: str) -> Dict[str, Any]:
    """
    Find recent changes for a service.

    Args:
        service_name: The name of the service to look up (e.g. "Payment API").

    Returns:
        A dict with "service_name", "count", and "changes", each including
        change_id, change_type, risk, implemented_at, summary, and
        rollback_available.
    """
    changes = _sorted_by_recency(_load_data())

    matches = [
        c for c in changes
        if str(c.get("service_name", "")).lower() == service_name.lower()
    ]

    summarized = [
        {
            "change_id": c.get("change_id", ""),
            "change_type": c.get("change_type", ""),
            "risk": c.get("risk", ""),
            "implemented_at": c.get("implemented_at", ""),
            "summary": c.get("summary", ""),
            "rollback_available": c.get("rollback_available", False),
        }
        for c in matches
    ]

    return {
        "service_name": service_name,
        "count": len(summarized),
        "changes": summarized,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
