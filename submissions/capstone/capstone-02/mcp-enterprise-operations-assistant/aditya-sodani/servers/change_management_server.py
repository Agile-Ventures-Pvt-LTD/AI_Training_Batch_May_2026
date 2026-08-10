import json
from pathlib import Path
from typing import Any

from src.config import CHANGE_FILE
from fastmcp import FastMCP
from src.mcp_logger import log_tool

mcp = FastMCP("change-management")

def load_json(file_path: Path) -> dict[str, Any]:
   
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {file_path}") from exc
    

class ChangeService:
    """
    Business logic for Change Management operations.
    """

    def __init__(self) -> None:
        self.data = load_json(CHANGE_FILE)

    def list_recent_changes(self) -> list[dict]:
        """
        Return all recent changes.
        """
        result = self.data["changes"]

        log_tool(
            "change_management",
            "list_recent_changes",
            result
        )

        return result

    def get_change_details(self, change_id: str) -> dict:
        """
        Return details of a specific change.
        """

        for change in self.data["changes"]:
            if change["change_id"] == change_id:
                return {
                    "found": True,
                    **change,
                }

        result = {
            "found": False,
            "message": f"{change_id} not found."
        }

        log_tool(
            "change_management",
            "get_change_details",
            result
        )

        return result

    def get_changes_for_service(self, service_name: str) -> list[dict]:
        """
        Return all changes for a service.
        """

        result = [
            change
            for change in self.data["changes"]
            if change["service_name"].lower() == service_name.lower()
        ]
        print("get changes for service :")
        print(type(result))
        print(result)
        log_tool(
            "change_management",
            "get_changes_for_service",
            result
        )

        return result
    

service = ChangeService()


@mcp.tool
def list_recent_changes() -> list[dict]:
    """
    List recent changes.
    """
    return service.list_recent_changes()


@mcp.tool
def get_change_details(change_id: str) -> dict:
    """
    Get change details.
    """
    return service.get_change_details(change_id)


@mcp.tool
def get_changes_for_service(service_name: str) -> list[dict]:
    """
    Return all changes for a service.
    """
    return service.get_changes_for_service(service_name)


if __name__ == "__main__":
    mcp.run()