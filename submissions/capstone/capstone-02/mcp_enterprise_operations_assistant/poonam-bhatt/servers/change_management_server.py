import sys
import os
# Add parent directory to sys.path to resolve src imports when run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastmcp import FastMCP
import src.tool_discovery as td

mcp = FastMCP("change-management")

@mcp.tool
def list_recent_changes(limit: int = 10) -> dict:
    """Return recent change records, ordered from most recent to oldest."""
    return td.list_recent_changes(limit)

@mcp.tool
def get_change_details(change_id: str) -> dict:
    """Return details of a specific change."""
    return td.get_change_details(change_id)

@mcp.tool
def get_changes_for_service(service_name: str) -> dict:
    """Find recent changes for a service, ordered from most recent to oldest."""
    return td.get_changes_for_service(service_name)

if __name__ == "__main__":
    mcp.run()
