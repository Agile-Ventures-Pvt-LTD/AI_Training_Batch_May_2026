import sys
import pytest
from pathlib import Path
from mcp_use import MCPClient
from src.config import config

sys.path.append(str(Path(__file__).resolve().parent.parent))

@pytest.mark.asyncio
async def test_mcp_tool_discovery():
    client=MCPClient(config)
    try:
        await client.create_all_sessions()
        server_names=client.get_server_names()
        assert "service-health" in server_names
        assert "support-ticket" in server_names
        assert "change-management" in server_names

        sh_session=client.get_session("service-health")
        sh_tools=await sh_session.list_tools()
        sh_tool_names=[t.name for t in sh_tools]
        assert "list_services" in sh_tool_names
        assert "get_service_health" in sh_tool_names
        assert "get_active_incidents" in sh_tool_names

        st_session=client.get_session("support-ticket")
        st_tools=await st_session.list_tools()
        st_tool_names=[t.name for t in st_tools]
        assert "search_tickets" in st_tool_names
        assert "get_ticket_details" in st_tool_names
        assert "get_high_priority_tickets" in st_tool_names

        cm_session=client.get_session("change-management")
        cm_tools=await cm_session.list_tools()
        cm_tool_names=[t.name for t in cm_tools]
        assert "list_recent_changes" in cm_tool_names
        assert "get_change_details" in cm_tool_names
        assert "get_changes_for_services" in cm_tool_names

    finally:
        await client.close_all_sessions()
