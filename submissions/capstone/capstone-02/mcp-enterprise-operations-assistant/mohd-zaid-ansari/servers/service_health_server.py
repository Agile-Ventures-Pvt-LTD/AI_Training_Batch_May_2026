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

service_health_path=DATASET_PATH/ "service_health.json"

mcp=FastMCP()

def load() -> Dict[str, Any]:
    return json.loads(Path(service_health_path).read_text(encoding="utf-8"))


@mcp.tool
async def list_services() -> Dict[str, Any]:
    """List all services and their current health status."""
    data = load()
    services = data.get("services", [])

    simplified = []
    for service in services:
        simplified.append(
            {
                "service_name": service.get("service_name"),
                "status": service.get("status"),
                "region":service.get("region"),
            }
        )

    return {"count": len(simplified), "services": simplified}

#==========================================================================================================================

@mcp.tool
async def get_service_health(service_name: str) -> Dict[str, Any]:
    """Return detailed health information for one service."""
    data = load()
    for svc in data.get("services", []):
        if svc.get("service_name") == service_name:
            return {
                "found": True,
                "service": svc,
            }
        
    return {
        "found": False,
        "message": "Service not found.",
    }

#============================================================================================================================

@mcp.tool
async def get_active_incidents(service_name: str = None) -> Dict[str, Any]:
    """Return active operational incidents."""
    data = load()
    incidents = data.get("incidents", [])

    active = []
    for incident in incidents:
        if incident.get("status") != "ACTIVE":
            continue
        if service_name and incident.get("service_name") != service_name:
            continue
        active.append(incident)

    return {
        "count": len(active),
        "incidents": active,
    }


if __name__=="__main__":
    mcp.run()






