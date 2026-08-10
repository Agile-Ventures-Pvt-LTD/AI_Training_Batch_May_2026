import pytest
from src.host import MCPClient


EXPECTED_DISCOVERED_TOOLS = {
    {
        "list_services",
        "get_service_health",
        "get_active_incident",
    },
    {
        "search_tickets",
        "get_ticket_details",
        "get_high_priority_tickets",
    },
    {
        "list_recent_changes",
        "get_change_details",
        "get_changes_for_service"
    }
    
}


@pytest.mark.asyncio
async def tool_discovery():
    """
    Verify that all required MCP tools are available.
    """

    client = MCPClient()

    try:
        await client.connect()

        tools = await client.list_tools()

        tool_names = {tool.name for tool in tools}

        missing_tools = EXPECTED_DISCOVERED_TOOLS - tool_names

        assert (
            not missing_tools
        ), f"Missing tools: {missing_tools}"

    finally:
        await client.disconnect()


    return{
        EXPECTED_DISCOVERED_TOOLS
        }