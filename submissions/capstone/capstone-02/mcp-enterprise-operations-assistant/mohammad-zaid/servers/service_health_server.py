import json
import sys
from fastmcp import FastMCP
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import HEALTH_FILE

shs_mcp = FastMCP("Service Health MCP Server")


def _load_health_data() -> dict:
    if not HEALTH_FILE.exists():
        return {"services": [], "incidents": []}
    with open(HEALTH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@shs_mcp.tool
def list_services() -> dict:
    """List all services and their current health status."""
    data = _load_health_data()
    summary = [
        {
            "service_name": s.get("service_name"),
            "status": s.get("status"),
            "region": s.get("region"),
        }
        for s in data.get("services", [])
    ]
    return {"count": len(summary), "services": summary}


@shs_mcp.tool
def get_service_health(service_name: str) -> dict:
    """Return detailed health information for one service."""
    try:
        data = _load_health_data()
        for s in data.get("services", []):
            if s.get("service_name", "").lower() == service_name.lower():
                return {"found": True, "service": s}
        return {"found": False, "message": "Service not found."}
    except Exception as e:
        return {"found": False, "message": f"Error: {e}"}


@shs_mcp.tool
def get_active_incidents(service_name: str = None) -> dict:
    """Return active operational incidents, optionally filtered by service."""
    data = _load_health_data()
    active = [inc for inc in data.get("incidents", []) if inc.get("status") == "ACTIVE"]

    if service_name:
        active = [inc for inc in active if inc.get("service_name", "").lower() == service_name.lower()]

    return {"count": len(active), "incidents": active}


if __name__ == "__main__":
    shs_mcp.run()