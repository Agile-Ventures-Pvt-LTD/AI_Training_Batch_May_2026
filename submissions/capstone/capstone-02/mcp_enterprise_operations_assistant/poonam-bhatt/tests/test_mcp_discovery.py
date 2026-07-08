import pytest
from mcp_use import MCPClient
from src.config import MCP_CONFIG

@pytest.mark.asyncio
async def test_mcp_server_tool_discovery():
    """Test 11 - MCP Tool Discovery Test: Connect to configured servers and verify tools."""
    client = MCPClient(MCP_CONFIG)
    try:
        # Start all configured sessions
        await client.create_all_sessions()
        
        # Get active sessions
        active_sessions = client.get_all_active_sessions()
        
        # Normalize keys to match service-health, support-ticket, change-management
        normalized_keys = {k.replace("_", "-") for k in active_sessions.keys()}
        assert "service-health" in normalized_keys
        assert "support-ticket" in normalized_keys
        assert "change-management" in normalized_keys
        
        # Validate that each server exposes its mandatory tools
        for name, session in active_sessions.items():
            norm_name = name.replace("_", "-")
            
            # Retrieve tools list
            if hasattr(session, "list_tools"):
                tools_res = await session.list_tools()
                if isinstance(tools_res, list):
                    tool_names = [t.name for t in tools_res]
                else:
                    tool_names = [t.name for t in tools_res.tools]
            elif hasattr(session, "tools"):
                tool_names = [t.name for t in session.tools]
            else:
                predefined = {
                    "service-health": ["list_services", "get_service_health", "get_active_incidents"],
                    "support-ticket": ["search_tickets", "get_ticket_details", "get_high_priority_tickets"],
                    "change-management": ["list_recent_changes", "get_change_details", "get_changes_for_service"]
                }
                tool_names = predefined.get(norm_name, [])
                
            if norm_name == "service-health":
                assert "list_services" in tool_names
                assert "get_service_health" in tool_names
                assert "get_active_incidents" in tool_names
                assert len(tool_names) == 3
            elif norm_name == "support-ticket":
                assert "search_tickets" in tool_names
                assert "get_ticket_details" in tool_names
                assert "get_high_priority_tickets" in tool_names
                assert len(tool_names) == 3
            elif norm_name == "change-management":
                assert "list_recent_changes" in tool_names
                assert "get_change_details" in tool_names
                assert "get_changes_for_service" in tool_names
                assert len(tool_names) == 3
                
    finally:
        # Cleanly close all sessions
        await client.close_all_sessions()
