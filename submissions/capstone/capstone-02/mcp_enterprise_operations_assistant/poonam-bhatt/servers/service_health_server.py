import sys
import os
# Add parent directory to sys.path to resolve src imports when run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Optional
from fastmcp import FastMCP
import src.tool_discovery as td

mcp = FastMCP("service-health")

@mcp.tool
def list_services() -> dict:
    """List all services and their current health status."""
    return td.list_services()

@mcp.tool
def get_service_health(service_name: str) -> dict:
    """Return detailed health information for one service."""
    return td.get_service_health(service_name)

@mcp.tool
def get_active_incidents(service_name: Optional[str] = None) -> dict:
    """Return active operational incidents, optionally filtered by service name."""
    return td.get_active_incidents(service_name)

if __name__ == "__main__":
    mcp.run()
