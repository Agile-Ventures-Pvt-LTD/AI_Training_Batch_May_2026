import os
import pytest
import asyncio
from unittest.mock import patch, MagicMock
from src.mcp_client import MCPClientManager
from src.host import handle_user_query

SERVER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../server/jira_mcp_server.py"))

@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_mcp_server_runs():
    client = MCPClientManager(SERVER_PATH)
    try:
        tools = await client.connect()
        assert len(tools) > 0
    finally:
        await client.disconnect()

@pytest.mark.asyncio
async def test_tool_discovery():
    client = MCPClientManager(SERVER_PATH)
    try:
        tools = await client.connect()
        assert "list_projects" in tools
        assert "search_issues" in tools
        assert "get_issues_details" in tools
        assert "get_issue_comments" in tools
        assert "add_issue_comment" in tools
        assert "update_issue_status" in tools
    finally:
        await client.disconnect()

@pytest.mark.asyncio
async def test_query_execution_read_format():
    result = await handle_user_query("List all Jira projects")
    assert "user_query" in result
    assert "tools_used" in result
    assert "final_answer" in result
    assert "write_action_performed" in result
    assert isinstance(result["tools_used"], list)
    assert result["write_action_performed"] is False

@pytest.mark.asyncio
async def test_query_execution_write_tracking():
    result = await handle_user_query("Add a comment saying 'Test' to issue INVALID-999")
    assert "user_query" in result
    assert "tools_used" in result
    assert "final_answer" in result
    if "add_issue_comment" in result["tools_used"]:
        assert result["write_action_performed"] is True

@pytest.mark.asyncio
async def test_invalid_issue_key_handling():
    client = MCPClientManager(SERVER_PATH)
    try:
        await client.connect()
        output = await client.execute_tool("get_issues_details", {"issue_key": "NONEXISTENTKEY123"})
        assert "Error" in output or "exist" in output or "HTTP" in output
    finally:
        await client.disconnect()

@pytest.mark.asyncio
async def test_search_issues_parameter_passing():
    client = MCPClientManager(SERVER_PATH)
    try:
        await client.connect()
        output = await client.execute_tool("search_issues", {"jql": "project is empty"})
        assert isinstance(output, str)
    finally:
        await client.disconnect()