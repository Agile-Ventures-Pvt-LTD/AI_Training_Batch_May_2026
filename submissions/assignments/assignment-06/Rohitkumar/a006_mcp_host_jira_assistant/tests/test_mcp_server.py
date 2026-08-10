import os
import sys
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_mcp_server_runs():
    """Test that the MCP server can be instantiated."""
    from server.jira_mcp_server import mcp
    assert mcp is not None
    assert mcp.name == "Jira MCP Server"


def test_tool_discovery():
    """Test that all expected tools are registered on the MCP server."""
    import asyncio
    from server.jira_mcp_server import mcp

    tools = asyncio.run(mcp.local_provider.list_tools())
    tool_names = [t.name for t in tools]
    expected_tools = [
        "list_projects", "search_issues", "get_issue_details",
        "get_issue_comments", "add_issue_comment", "update_issue_status",
        "get_available_transitions"
    ]
    for tool in expected_tools:
        assert tool in tool_names


@patch("server.jira_mcp_server._request")
def test_list_projects_returns_dict(mock_request):
    """Test that list_projects wraps list response in a dict."""
    mock_request.return_value = [{"key": "TEST", "name": "Test"}]
    from server.jira_mcp_server import list_projects
    result = list_projects()
    assert isinstance(result, dict)
    assert "projects" in result
    assert result["total"] == 1


@patch("server.jira_mcp_server._request")
def test_query_execution(mock_request):
    """Test that a tool executes and returns a result."""
    mock_request.return_value = {"issues": []}
    from server.jira_mcp_server import search_issues
    result = search_issues("project = TEST")
    assert isinstance(result, dict)


@patch("server.jira_mcp_server._request")
def test_multi_tool_flow(mock_request):
    """Test using multiple tools in sequence."""
    from server.jira_mcp_server import search_issues, get_issue_details

    mock_request.return_value = {"issues": [{"key": "TEST-1"}]}
    search_result = search_issues("project IS NOT EMPTY", max_results=5)
    assert search_result["issues"][0]["key"] == "TEST-1"

    mock_request.return_value = {"key": "TEST-1", "fields": {"summary": "Test"}}
    detail = get_issue_details("TEST-1")
    assert detail["key"] == "TEST-1"


@patch("server.jira_mcp_server._request")
def test_write_operation(mock_request):
    """Test that write operations work."""
    mock_request.return_value = {"id": "1"}
    from server.jira_mcp_server import add_issue_comment
    result = add_issue_comment("TEST-1", "Test comment")
    assert isinstance(result, dict)
    assert result["id"] == "1"