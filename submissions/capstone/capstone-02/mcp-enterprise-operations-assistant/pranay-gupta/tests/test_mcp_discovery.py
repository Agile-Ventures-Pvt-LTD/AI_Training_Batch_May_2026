import pytest
import sys
from pathlib import Path

# sys.path.insert(0, str(Path(__file__).parent.parent))
from src.config import MCP_SERVER_CONFIG

@pytest.mark.asyncio
async def test_mcp_tool_discovery():
    from mcp_use import MCPClient
    
    client = MCPClient(MCP_SERVER_CONFIG)
    discovered = {}
    
    for server_name in MCP_SERVER_CONFIG["mcpServers"].keys():
        session = await client.create_session(server_name)
        await session.connect()
        tools = await session.list_tools()
        discovered[server_name] = [tool.name for tool in tools]
        # await session.close()
        
    await client.close_all_sessions()
    
    assert len(discovered.get("service-health", [])) == 3
    assert set(discovered["service-health"]) == {"list_services", "get_service_health", "get_active_incidents"}
    
    assert len(discovered.get("support-ticket", [])) == 3
    assert set(discovered["support-ticket"]) == {"search_tickets", "get_ticket_details", "get_high_priority_tickets"}
    
    assert len(discovered.get("change-management", [])) == 3
    assert set(discovered["change-management"]) == {"list_recent_changes", "get_change_details", "get_changes_for_service"}