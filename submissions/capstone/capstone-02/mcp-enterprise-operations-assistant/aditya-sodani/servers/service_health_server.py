import json
from pathlib import Path
from typing import Any
from src.mcp_logger import log_tool

from src.config import SERVICE_HEALTH_FILE
from fastmcp import FastMCP

mcp = FastMCP("service-health")


def load_json(file_path: Path) -> dict[str, Any]:
   
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {file_path}") from exc
    

class ServiceHealthService:
    """Business logic for service health operations."""

    def __init__(self) -> None:
        self.data = load_json(SERVICE_HEALTH_FILE)

    def list_services(self) -> list[dict]:
        """Return all services."""

        result = [
            {
                "service_name": service["service_name"],
                "status": service["status"],
                "region": service["region"],
            }
            for service in self.data["services"]
        ]

        log_tool(
            "service_health",
            "list_services",
            result
        )

        return result

    def get_service_health(self, service_name: str) -> dict:
        """Return health details for one service."""

        for service in self.data["services"]:
            if service["service_name"].lower() == service_name.lower():
                return {
                    "found": True,
                    **service,
                }

        result = {
            "found": False,
            "message": f"'{service_name}' not found.",
        }

        log_tool(
            "service_health",
            "get_service_health",
            result
        )

        return result

    def get_active_incidents(self, service_name: str | None = None) -> list[dict]:
        """Return active incidents."""

        incidents = self.data["incidents"]

        if service_name:
            incidents = [
                incident
                for incident in incidents
                if incident["service_name"].lower() == service_name.lower()
            ]

        result = [
            incident
            for incident in incidents
            if incident["status"] == "ACTIVE"
        ]
        print("get active incidents:")
        print(type(result))
        print(result)

        log_tool(
            "service_health",
            "get_active_incidents",
            result
        )

        return result
    

service = ServiceHealthService()


@mcp.tool
def list_services() -> list[dict]:
    """
    List all enterprise services.
    """
    return service.list_services()


@mcp.tool
def get_service_health(service_name: str) -> dict:
    """
    Get detailed health information for a specific service.

    Required Input:
    service_name: Name of the service.

    Example:
    service_name:"Payment API"
    """
    return service.get_service_health(service_name)


@mcp.tool
def get_active_incidents(service_name: str | None = None) -> list[dict]:
    """
    Return active incidents.

    Optional input:
    service_name

    Example:
    service_name:"Payment API"

    if no service_name is provided,
    return all active incidents.
    """
    return service.get_active_incidents(service_name)


if __name__ == "__main__":
    mcp.run()