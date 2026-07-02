import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mcp_client import MCPClientManager

SERVER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../server/jira_mcp_server.py"))

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def connected_mcp_client():
    client = MCPClientManager(SERVER_PATH)
    await client.connect()
    yield client
    await client.disconnect()

@pytest.mark.anyio
async def test_all_expected_tools_are_registered(connected_mcp_client):
    discovered_tools = [tool.name for tool in connected_mcp_client.tools]
    expected_tools = [
        "list_projects",
        "search_issues",
        "get_issues_details",
        "get_issue_comments",
        "add_issue_comment",
        "update_issue_status"
    ]
    for tool_name in expected_tools:
        assert tool_name in discovered_tools, f"Required tool '{tool_name}' was not discovered on the MCP Server."

@pytest.mark.anyio
async def test_search_issues_schema_arguments(connected_mcp_client):
    target_tool = next((t for t in connected_mcp_client.tools if t.name == "search_issues"), None)
    assert target_tool is not None
    schema_properties = target_tool.inputSchema.get("properties", {})
    assert "jql" in schema_properties, "Tool 'search_issues' is missing the required 'jql' parameter."
    assert schema_properties["jql"]["type"] == "string"

@pytest.mark.anyio
async def test_add_comment_schema_arguments(connected_mcp_client):
    target_tool = next((t for t in connected_mcp_client.tools if t.name == "add_issue_comment"), None)
    assert target_tool is not None
    schema_properties = target_tool.inputSchema.get("properties", {})
    assert "issue_key" in schema_properties, "Tool 'add_issue_comment' is missing 'issue_key' parameter."
    assert "comment" in schema_properties, "Tool 'add_issue_comment' is missing 'comment' parameter."

@pytest.mark.anyio
async def test_update_status_schema_arguments(connected_mcp_client):
    target_tool = next((t for t in connected_mcp_client.tools if t.name == "update_issue_status"), None)
    assert target_tool is not None
    schema_properties = target_tool.inputSchema.get("properties", {})
    assert "issue_key" in schema_properties, "Tool 'update_issue_status' is missing 'issue_key' parameter."
    assert "transition_id" in schema_properties, "Tool 'update_issue_status' is missing 'transition_id' parameter."

@pytest.mark.anyio
async def test_tools_have_valid_descriptions(connected_mcp_client):
    for tool in connected_mcp_client.tools:
        assert tool.description is not None, f"Tool '{tool.name}' is missing a docstring description definition."
        assert len(tool.description.strip()) > 10, f"Tool '{tool.name}' description is too short for semantic mapping."