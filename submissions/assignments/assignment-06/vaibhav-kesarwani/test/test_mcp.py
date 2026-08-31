import pytest
from unittest.mock import AsyncMock, patch
from src.host import MCPHost


@pytest.fixture
def mock_host():
    with patch("host.MCPAgent") as mock_agent:
        instance = mock_agent.return_value
        host = MCPHost()

        host.agent = instance

        yield host


@pytest.mark.asyncio
async def test_mcp_server_runs(mock_host):
    assert mock_host is not None
    assert mock_host.agent is not None


@pytest.mark.asyncio
async def test_tool_discovery(mock_host):
    mock_host.tool_tracker.tools = [
        "list_projects",
        "search_issues",
        "get_issue_details",
        "get_issue_comments",
        "add_issue_comment",
        "update_issue_status"
    ]

    expected_tools = {
        "list_projects",
        "search_issues",
        "get_issue_details",
        "get_issue_comments",
        "add_issue_comment",
        "update_issue_status"
    }

    assert mock_host.tool_tracker.tools == expected_tools


@pytest.mark.asyncio
async def test_query_execution(mock_host):
    mock_host.agent.run = AsyncMock(
        return_value="Found 2 projects"
    )

    mock_host.tool_tracker.tools = ["list_projects"]

    result = await mock_host.run("List projects")

    assert (result["final_answer"] == "Found 2 projects")
    assert ("list_projects" in result["tools_used"])


@pytest.mark.asyncio
async def test_multi_tool_flow(mock_host):
    mock_host.agent.run = AsyncMock(
        return_value="Found issue details"
    )

    mock_host.tool_tracker.tools = [
        "search_issues",
        "get_issue_details"
    ]

    result = await mock_host.run("Find AI-101 details")

    assert len(result["tools_used"]) == 2
    assert ("search_issues" in result["tools_used"])
    assert ("get_issue_details" in result["tools_used"])


@pytest.mark.asyncio
async def test_write_operation(mock_host):
    mock_host.agent.run = AsyncMock(
        return_value="Comment added successfully"
    )

    mock_host.tool_tracker.tools = ["add_issue_comment"]

    result = await mock_host.run("Add comment to AI-101")

    assert (result["write_action_performed"] is True)
    assert ("add_issue_comment" in result["tools_used"])