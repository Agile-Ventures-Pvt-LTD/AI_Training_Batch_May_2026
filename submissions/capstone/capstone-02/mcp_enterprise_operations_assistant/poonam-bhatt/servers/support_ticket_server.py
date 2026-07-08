import sys
import os
# Add parent directory to sys.path to resolve src imports when run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Optional
from fastmcp import FastMCP
import src.tool_discovery as td

mcp = FastMCP("support-ticket")

@mcp.tool
def search_tickets(service_name: Optional[str] = None, priority: Optional[str] = None, status: Optional[str] = None, limit: int = 50) -> dict:
    """Search support tickets using predefined filters."""
    return td.search_tickets(service_name, priority, status, limit)

@mcp.tool
def get_ticket_details(ticket_id: str) -> dict:
    """Get full details of one support ticket."""
    return td.get_ticket_details(ticket_id)

@mcp.tool
def get_high_priority_tickets(service_name: Optional[str] = None) -> dict:
    """Return open P1 and P2 tickets, optionally filtered by service name."""
    return td.get_high_priority_tickets(service_name)

if __name__ == "__main__":
    mcp.run()
