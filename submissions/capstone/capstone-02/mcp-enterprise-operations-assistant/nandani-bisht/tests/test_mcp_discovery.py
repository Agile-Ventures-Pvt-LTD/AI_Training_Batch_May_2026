import pytest
from mcp_use import MCPClient
from src.config import MCP_CONFIG

@pytest.mark.asyncio
async def test_mcp_tool_discovery():
    """Verify tool discovery connects and lists 3 expected tools on each server."""
    client = MCPClient(MCP_CONFIG)
    try:
        await client.create_all_sessions()
        
        
        sh_session = client.sessions.get("service-health")
        assert sh_session is not None
        sh_tools = await sh_session.list_tools()
        sh_tool_names = [t.name for t in sh_tools]
        assert len(sh_tool_names) == 3
        assert "list_services" in sh_tool_names
        assert "get_service_health" in sh_tool_names
        assert "get_active_incidents" in sh_tool_names
        
        
        st_session = client.sessions.get("support-ticket")
        assert st_session is not None
        st_tools = await st_session.list_tools()
        st_tool_names = [t.name for t in st_tools]
        assert len(st_tool_names) == 3
        assert "search_tickets" in st_tool_names
        assert "get_ticket_details" in st_tool_names
        assert "get_high_priority_tickets" in st_tool_names
        
        
        cm_session = client.sessions.get("change-management")
        assert cm_session is not None
        cm_tools = await cm_session.list_tools()
        cm_tool_names = [t.name for t in cm_tools]
        assert len(cm_tool_names) == 3
        assert "list_recent_changes" in cm_tool_names
        assert "get_change_details" in cm_tool_names
        assert "get_changes_for_service" in cm_tool_names
        
    finally:
        await client.close_all_sessions()
