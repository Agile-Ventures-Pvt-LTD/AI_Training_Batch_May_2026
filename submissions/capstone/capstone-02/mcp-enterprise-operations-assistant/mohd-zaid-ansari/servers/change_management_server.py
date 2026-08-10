import argparse
import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any
from dotenv import load_dotenv
load_dotenv()
from fastmcp import FastMCP

BASE_DIR=Path(__file__).resolve().parent.parent
DATASET_PATH=BASE_DIR/ "data"

changes_path=DATASET_PATH/ "changes.json"

mcp=FastMCP()

def load() -> List[Dict[str, Any]]:
    # changes.json schema: {"changes": [ ... ]}
    data = json.loads(Path(changes_path).read_text(encoding="utf-8"))
    return data.get("changes", [])

@mcp.tool
async def list_recent_changes(limit: int = 10) -> Dict[str, Any]:
    """Return recent change records."""
    changes = load()

    changes_sorted = sorted(
        changes,
        key=lambda chng: str(chng.get("implemented_at", "")),
        reverse=True,
    )
    recent = changes_sorted[:limit]
    return {
        "count": len(recent),
        "changes": recent,
    }

#===========================================================================================================================

@mcp.tool
async def get_change_details(change_id: str) -> Dict[str, Any]:
    """Return details of a specific change."""
    changes = load()

    for ch in changes:
        if str(ch.get("change_id")) == str(change_id):
            return {
                "found": True,
                "change": ch,
            }

    return {
        "found": False,
        "message": "Change not found.",
    }

#===========================================================================================================================

@mcp.tool
async def get_changes_for_service(service_name: str) -> Dict[str, Any]:
    """Find recent changes for a service."""
    changes = load()

    matched = [ch for ch in changes if str(ch.get("service_name")) == str(service_name)]
    matched_sorted = sorted(
        matched,
        key=lambda chng: str(chng.get("implemented_at", "")),
        reverse=True,
    )
    return {
        "service_name": service_name,
        "count": len(matched_sorted),
        "changes": matched_sorted,
    }


if __name__ == "__main__":
    mcp.run()
