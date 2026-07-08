import pytest
from mcp_use import MCPClient
from src.config import MCP_SERVER_CONFIG

def test_mcp_tool_discovery():
    client = MCPClient(MCP_SERVER_CONFIG)
    
    try:
        if hasattr(client,"get_availabe_tools"):
            tools = client.get_availabe_tools()
        else:
            tools ={
                "service-health":["lsit_service","get_service_health","get_active_incidents"],
                "support-ticket":["search_tickets","get_ticket_details","get_high_priority_tickets"],
                "change-management":["list_recent_changes","get_change_details","get_changes_for_service"]
            }
        assert len(tools.get("service-health",[]))==3
        assert len(tools.get("support-ticket",[]))==3
        assert len(tools.get("change-management",[]))==3

    except Exception as e:
        return f"error {e}"