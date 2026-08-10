from server.jira_mcp_server import mcp
import asyncio

EXPECTED_TOOLS = {
    "list_projects",
    "search_issues",
    "get_issue_details",
    "get_issue_comments",
    "add_issue_comment",
    "update_issue_status",
}


# Verifying MCP server initializes.
def test_mcp_server_runs():
    assert mcp is not None


# Verifying all tools are registered.
def test_tool_discovery():
    async def run():
        tools = await mcp._list_tools()
        tool_names = {tool.name for tool in tools}
        assert EXPECTED_TOOLS.issubset(tool_names)
    
    asyncio.run(run())