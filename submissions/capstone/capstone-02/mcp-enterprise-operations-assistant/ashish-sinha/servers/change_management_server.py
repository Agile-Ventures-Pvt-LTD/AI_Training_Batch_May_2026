import json
import logging
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP
from src.config import CHANGE_PATH

logging.basicConfig(level=logging.ERROR)

mcp = FastMCP("Change_Management_MCP_Server")

def load_change_path_json() -> List[Any]:
    with open(CHANGE_PATH, "r", encoding="utf-8") as data_file:
        raw_data = json.load(data_file)
        if isinstance(raw_data, dict):
            if "changes" in raw_data:
                return raw_data["changes"]
            return list(raw_data.values())
        if isinstance(raw_data, list):
            return raw_data
        return []

@mcp.tool
def list_recent_changes(limit: int = 10) -> Dict[str, Any]:
    records = load_change_path_json()
    valid_records = [r for r in records if isinstance(r, dict)]
    sorted_records = sorted(valid_records, key=lambda x: x.get("implemented_at", ""), reverse=True)
    selected = sorted_records[:limit]
    extracted = []
    for item in selected:
        extracted.append({
            "change_id": item.get("change_id"),
            "service_name": item.get("service_name"),
            "change_type": item.get("change_type"),
            "status": item.get("status"),
            "risk": item.get("risk"),
            "implemented_at": item.get("implemented_at")
        })
    return {"count": len(extracted), "changes": extracted}

@mcp.tool
def get_change_details(change_id: str) -> Dict[str, Any]:
    records = load_change_path_json()
    for item in records:
        if isinstance(item, dict) and item.get("change_id") == change_id:
            return {"found": True, "change": item}
    return {"found": False, "message": "Change record not found"}

@mcp.tool
def get_changes_for_service(service_name: str) -> Dict[str, Any]:
    records = load_change_path_json()
    matched = []
    for item in records:
        if isinstance(item, dict) and item.get("service_name") == service_name:
            matched.append({
                "change_id": item.get("change_id"),
                "change_type": item.get("change_type"),
                "risk": item.get("risk"),
                "implemented_at": item.get("implemented_at"),
                "summary": item.get("summary"),
                "rollback_available": item.get("rollback_available")
            })
    return {"service_name": service_name, "count": len(matched), "changes": matched}

if __name__ == "__main__":
    mcp.run()
