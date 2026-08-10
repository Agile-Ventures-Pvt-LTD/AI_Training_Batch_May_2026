import pytest
from pathlib import Path
from fastmcp import Client

PROJECT_ROOT=Path(__file__).resolve().parent.parent
SERVER_PATH=PROJECT_ROOT/ "server" / "jira_mcp_server.py"

@pytest.mark.asyncio
async def test_mcp_server():
    client=Client(SERVER_PATH)
    async with client:
        tool=await client.list_tools()
        tool_names=[tool.name for tool in tool]
        assert "list_projects" in tool_names
        assert "search_issues" in tool_names
        assert "get_issue_details" in tool_names
        assert "get_issue_comments" in tool_names
        assert "add_issue_comment" in tool_names
        assert "update_issue_status" in tool_names