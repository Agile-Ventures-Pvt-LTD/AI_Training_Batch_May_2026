import os
import sys
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_mcp_discovery_for_service_health ():
    """Test that all expected tools are registered on the Service Health MCP server."""
    import asyncio
    from servers.service_health_server import mcp

    tools = asyncio.run(mcp.local_provider.list_tools())
    tool_names = [t.name for t in tools]
    expected_tools = [
        'list_services', 'get_services_health', 'get_active_incidents'
    ]
    for tool in expected_tools:
        assert tool in tool_names

def test_mcp_discovery_for_Change ():
    """Test that all expected tools are registered on Change Management  MCP server."""
    import asyncio
    from servers.service_health_server import mcp

    tools = asyncio.run(mcp.local_provider.list_tools())
    tool_names = [t.name for t in tools]
    expected_tools = [
        'list_recent_changes','get_change_details','get_changes_for_service'
         ]
    for tool in expected_tools:
        assert tool in tool_names

def test_mcp_discovery_support_ticket():
    """Test that all expected tools are registered on Support Ticket   MCP server."""
    import asyncio
    from servers.service_health_server import mcp

    tools = asyncio.run(mcp.local_provider.list_tools())
    tool_names = [t.name for t in tools]
    expected_tools = [
        'search_tickets',"get_ticket_details",'get_high_priority_tickets'
        ]
    for tool in expected_tools:
        assert tool in tool_names



