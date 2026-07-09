## Service Health MCP Server
## Data source: data/service_health.json

from __future__ import annotations
import os
import json
from typing import Any, Optional, Dict, List
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

class ServiceHealthError(RuntimeError):
    """Raised when service health data cannot be read or is malformed."""

mcp = FastMCP(name="service-health")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "service_health.json")


def _load_data() -> Dict[str, Any]:
    """
    Load the service health dataset from disk.

    Returns:
        Parsed JSON as a dict with "services" and "incidents" keys.

    Raises:
        ServiceHealthError if the file is missing or malformed.
    """
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise ServiceHealthError(f"Data file not found at {DATA_PATH}")
    except json.JSONDecodeError as e:
        raise ServiceHealthError(f"Malformed service health data: {e}")

    if not isinstance(data, dict) or "services" not in data or "incidents" not in data:
        raise ServiceHealthError("Unexpected service health data shape.")

    return data


@mcp.tool
def list_services() -> Dict[str, Any]:
    """
    List all services and their current health status.

    Returns:
        A dict with "count" and "services", where each service includes
        service_name, status, and region.
    """
    data = _load_data()
    services = data.get("services", [])

    summarized = [
        {
            "service_name": s.get("service_name", ""),
            "status": s.get("status", ""),
            "region": s.get("region", ""),
        }
        for s in services
    ]

    return {
        "count": len(summarized),
        "services": summarized,
    }


@mcp.tool
def get_service_health(service_name: str) -> Dict[str, Any]:
    """
    Return detailed health information for one service.

    Args:
        service_name: The name of the service to look up (e.g. "Payment API").

    Returns:
        A dict with "found" and, if found, the full "service" record
        including error_rate_percent, average_latency_ms, cpu_usage_percent,
        memory_usage_percent, last_checked, and active_incident_ids.
    """
    data = _load_data()
    services = data.get("services", [])

    for s in services:
        if str(s.get("service_name", "")).lower() == service_name.lower():
            return {
                "found": True,
                "service": s,
            }

    return {
        "found": False,
        "message": "Service not found.",
    }


@mcp.tool
def get_active_incidents(service_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Return active operational incidents, optionally filtered by service.

    Args:
        service_name: Optional service name to filter incidents by.
            If omitted, all active incidents are returned.

    Returns:
        A dict with "count" and "incidents", each incident including
        incident_id, service_name, severity, status, summary,
        customer_impact, and assigned_group.
    """
    data = _load_data()
    incidents = data.get("incidents", [])

    active = [i for i in incidents if str(i.get("status", "")).upper() == "ACTIVE"]

    if service_name:
        active = [
            i for i in active
            if str(i.get("service_name", "")).lower() == service_name.lower()
        ]

    return {
        "count": len(active),
        "incidents": active,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
