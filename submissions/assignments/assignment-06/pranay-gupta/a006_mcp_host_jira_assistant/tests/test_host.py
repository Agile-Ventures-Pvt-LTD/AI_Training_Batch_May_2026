import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.host import user_query


@pytest.mark.asyncio
@patch("src.host.GroqEngine")
@patch("src.host.MCPClientManager")
async def test_user_query_read_operation(
    mock_client_cls,
    mock_engine_cls,
):
    mock_client = AsyncMock()
    mock_client.tools = []

    mock_client.connect.return_value = None

    mock_client.execute_tool.return_value = "TEST Project"

    mock_client.disconnect.return_value = None

    mock_client_cls.return_value = mock_client

    mock_engine = MagicMock()

    mock_engine.format_mcp_tools.return_value = []

    tool_call = MagicMock()

    tool_call.id = "tool_1"

    tool_call.function.name = "list_projects"

    tool_call.function.arguments = json.dumps({})

    first_message = MagicMock()

    first_message.tool_calls = [tool_call]

    second_message = MagicMock()

    second_message.tool_calls = None

    second_message.content = "Available project is TEST."

    first_response = MagicMock()

    first_response.choices = [
        MagicMock(message=first_message)
    ]

    second_response = MagicMock()

    second_response.choices = [
        MagicMock(message=second_message)
    ]

    mock_engine.generate_chat_response.side_effect = [
        first_response,
        second_response,
    ]

    mock_engine_cls.return_value = mock_engine

    result = await user_query(
        "List all projects"
    )

    assert result["user_query"] == "List all projects"

    assert "list_projects" in result["tools_used"]

    assert result["write_action_performed"] is False

    assert result["final_answer"] == "Available project is TEST."

    mock_client.connect.assert_awaited_once()

    mock_client.execute_tool.assert_awaited_once()

    mock_client.disconnect.assert_awaited_once()


@pytest.mark.asyncio
@patch("src.host.GroqEngine")
@patch("src.host.MCPClientManager")
async def test_user_query_write_operation(
    mock_client_cls,
    mock_engine_cls,
):
    mock_client = AsyncMock()

    mock_client.tools = []

    mock_client.connect.return_value = None

    mock_client.execute_tool.return_value = (
        "Success: Comment added."
    )

    mock_client.disconnect.return_value = None

    mock_client_cls.return_value = mock_client

    mock_engine = MagicMock()

    mock_engine.format_mcp_tools.return_value = []

    tool_call = MagicMock()

    tool_call.id = "tool_1"

    tool_call.function.name = "add_issue_comment"

    tool_call.function.arguments = json.dumps(
        {
            "issue_key": "TEST-1",
            "comment": "Done",
        }
    )

    first_message = MagicMock()

    first_message.tool_calls = [tool_call]

    second_message = MagicMock()

    second_message.tool_calls = None

    second_message.content = (
        "Comment added successfully."
    )

    first_response = MagicMock()

    first_response.choices = [
        MagicMock(message=first_message)
    ]

    second_response = MagicMock()

    second_response.choices = [
        MagicMock(message=second_message)
    ]

    mock_engine.generate_chat_response.side_effect = [
        first_response,
        second_response,
    ]

    mock_engine_cls.return_value = mock_engine

    result = await user_query(
        "Add comment"
    )

    assert result["write_action_performed"] is True

    assert result["tools_used"] == [
        "add_issue_comment"
    ]

    assert (
        result["final_answer"]
        == "Comment added successfully."
    )


@pytest.mark.asyncio
@patch("src.host.GroqEngine")
@patch("src.host.MCPClientManager")
async def test_user_query_without_tool_calls(
    mock_client_cls,
    mock_engine_cls,
):
    mock_client = AsyncMock()

    mock_client.tools = []

    mock_client.connect.return_value = None

    mock_client.disconnect.return_value = None

    mock_client_cls.return_value = mock_client

    mock_engine = MagicMock()

    mock_engine.format_mcp_tools.return_value = []

    assistant_message = MagicMock()

    assistant_message.tool_calls = None

    assistant_message.content = (
        "No Jira action required."
    )

    response = MagicMock()

    response.choices = [
        MagicMock(message=assistant_message)
    ]

    mock_engine.generate_chat_response.return_value = (
        response
    )

    mock_engine_cls.return_value = mock_engine

    result = await user_query(
        "Hello"
    )

    assert result["tools_used"] == []

    assert result["write_action_performed"] is False

    assert (
        result["final_answer"]
        == "No Jira action required."
    )

    mock_client.execute_tool.assert_not_called()


@pytest.mark.asyncio
@patch("src.host.GroqEngine")
@patch("src.host.MCPClientManager")
async def test_disconnect_called_on_exception(
    mock_client_cls,
    mock_engine_cls,
):
    mock_client = AsyncMock()

    mock_client.tools = []

    mock_client.connect.return_value = None

    mock_client.disconnect.return_value = None

    mock_client_cls.return_value = mock_client

    mock_engine = MagicMock()

    mock_engine.format_mcp_tools.return_value = []

    mock_engine.generate_chat_response.side_effect = Exception(
        "Groq Failure"
    )

    mock_engine_cls.return_value = mock_engine

    with pytest.raises(Exception):
        await user_query(
            "List projects"
        )

    mock_client.disconnect.assert_awaited_once()