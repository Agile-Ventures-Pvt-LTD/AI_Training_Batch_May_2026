import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.host import handle_user_query


@pytest.mark.asyncio
@patch("src.host.GroqEngine")
@patch("src.host.MCPClientManager")
async def test_end_to_end_read_flow(
    mock_client_cls,
    mock_engine_cls,
):
    mock_client = AsyncMock()

    mock_client.tools = []

    mock_client.connect.return_value = None

    mock_client.disconnect.return_value = None

    mock_client.execute_tool.return_value = (
        "[TEST-101] Login issue (Status: Open)"
    )

    mock_client_cls.return_value = mock_client

    mock_engine = MagicMock()

    mock_engine.format_mcp_tools.return_value = []

    tool_call = MagicMock()
    tool_call.id = "tool_1"
    tool_call.function.name = "search_issues"
    tool_call.function.arguments = json.dumps(
        {
            "jql": "status = Open"
        }
    )

    assistant_tool_message = MagicMock()
    assistant_tool_message.tool_calls = [tool_call]

    assistant_final_message = MagicMock()
    assistant_final_message.tool_calls = None
    assistant_final_message.content = (
        "There is one open Jira issue."
    )

    first_response = MagicMock()
    first_response.choices = [
        MagicMock(message=assistant_tool_message)
    ]

    second_response = MagicMock()
    second_response.choices = [
        MagicMock(message=assistant_final_message)
    ]

    mock_engine.generate_chat_response.side_effect = [
        first_response,
        second_response,
    ]

    mock_engine_cls.return_value = mock_engine

    result = await handle_user_query(
        "Show all open issues"
    )

    assert result["user_query"] == "Show all open issues"

    assert result["tools_used"] == [
        "search_issues"
    ]

    assert result["write_action_performed"] is False

    assert result["final_answer"] == (
        "There is one open Jira issue."
    )


@pytest.mark.asyncio
@patch("src.host.GroqEngine")
@patch("src.host.MCPClientManager")
async def test_end_to_end_write_flow(
    mock_client_cls,
    mock_engine_cls,
):
    mock_client = AsyncMock()

    mock_client.tools = []

    mock_client.connect.return_value = None

    mock_client.disconnect.return_value = None

    mock_client.execute_tool.return_value = (
        "Success: Comment added."
    )

    mock_client_cls.return_value = mock_client

    mock_engine = MagicMock()

    mock_engine.format_mcp_tools.return_value = []

    tool_call = MagicMock()
    tool_call.id = "tool_2"
    tool_call.function.name = "add_issue_comment"
    tool_call.function.arguments = json.dumps(
        {
            "issue_key": "TEST-10",
            "comment": "Completed"
        }
    )

    assistant_tool_message = MagicMock()
    assistant_tool_message.tool_calls = [tool_call]

    assistant_final_message = MagicMock()
    assistant_final_message.tool_calls = None
    assistant_final_message.content = (
        "Comment added successfully."
    )

    first_response = MagicMock()
    first_response.choices = [
        MagicMock(message=assistant_tool_message)
    ]

    second_response = MagicMock()
    second_response.choices = [
        MagicMock(message=assistant_final_message)
    ]

    mock_engine.generate_chat_response.side_effect = [
        first_response,
        second_response,
    ]

    mock_engine_cls.return_value = mock_engine

    result = await handle_user_query(
        "Add comment to TEST-10"
    )

    assert result["write_action_performed"] is True

    assert result["tools_used"] == [
        "add_issue_comment"
    ]

    assert result["final_answer"] == (
        "Comment added successfully."
    )


@pytest.mark.asyncio
@patch("src.host.GroqEngine")
@patch("src.host.MCPClientManager")
async def test_multiple_tool_execution(
    mock_client_cls,
    mock_engine_cls,
):
    mock_client = AsyncMock()

    mock_client.tools = []

    mock_client.connect.return_value = None

    mock_client.disconnect.return_value = None

    mock_client.execute_tool.side_effect = [
        "Issue Details",
        "Issue Comments",
    ]

    mock_client_cls.return_value = mock_client

    mock_engine = MagicMock()

    mock_engine.format_mcp_tools.return_value = []

    tool_call_1 = MagicMock()
    tool_call_1.id = "tool_1"
    tool_call_1.function.name = "get_issues_details"
    tool_call_1.function.arguments = json.dumps(
        {
            "issue_key": "TEST-1"
        }
    )

    tool_call_2 = MagicMock()
    tool_call_2.id = "tool_2"
    tool_call_2.function.name = "get_issue_comments"
    tool_call_2.function.arguments = json.dumps(
        {
            "issue_key": "TEST-1"
        }
    )

    assistant_tool_message = MagicMock()
    assistant_tool_message.tool_calls = [
        tool_call_1,
        tool_call_2,
    ]

    assistant_final_message = MagicMock()
    assistant_final_message.tool_calls = None
    assistant_final_message.content = (
        "Issue details and comments summarized."
    )

    first_response = MagicMock()
    first_response.choices = [
        MagicMock(message=assistant_tool_message)
    ]

    second_response = MagicMock()
    second_response.choices = [
        MagicMock(message=assistant_final_message)
    ]

    mock_engine.generate_chat_response.side_effect = [
        first_response,
        second_response,
    ]

    mock_engine_cls.return_value = mock_engine

    result = await handle_user_query(
        "Summarize TEST-1"
    )

    assert set(result["tools_used"]) == {
        "get_issues_details",
        "get_issue_comments",
    }

    assert (
        result["final_answer"]
        == "Issue details and comments summarized."
    )

    assert mock_client.execute_tool.await_count == 2