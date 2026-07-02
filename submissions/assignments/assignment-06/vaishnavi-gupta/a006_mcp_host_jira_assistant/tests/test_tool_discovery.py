import pytest
from src.mcp_client import JiraMCPClient


EXPECTED_TOOLS = {
    "list_projects",
    "search_issues",
    "get_issue_details",
    "get_issue_comments",
    "add_issue_comment",
    "update_issue_status",
}


@pytest.mark.asyncio
async def test_tool_discovery():
    """
    Verify that all required MCP tools are available.
    """

    client = JiraMCPClient()

    try:
        await client.connect()

        tools = await client.list_tools()

        tool_names = {tool.name for tool in tools}

        missing_tools = EXPECTED_TOOLS - tool_names

        assert (
            not missing_tools
        ), f"Missing tools: {missing_tools}"

    finally:
        await client.disconnect()

