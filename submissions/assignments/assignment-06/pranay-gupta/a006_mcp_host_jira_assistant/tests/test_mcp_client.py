from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.mcp_client import MCPClient


@pytest.mark.asyncio
@patch("src.mcp_client.ClientSession")
@patch("src.mcp_client.stdio_client")
async def test_connect(mock_stdio_client,mock_client_session,):
    client = MCPClient("server.py")

    read_stream = MagicMock()
    write_stream = MagicMock()

    client.exit_stack.enter_async_context = AsyncMock()

    client.exit_stack.enter_async_context.side_effect = [
        (read_stream, write_stream),
        AsyncMock(),
    ]

    session = client.exit_stack.enter_async_context.side_effect[1]

    tool = MagicMock()
    tool.name = "list_projects"

    tool_response = MagicMock()
    tool_response.tools = [tool]

    session.initialize = AsyncMock()
    session.list_tools = AsyncMock(return_value=tool_response)

    mock_client_session.return_value = session

    tools = await client.connect()

    assert tools == ["list_projects"]

    session.initialize.assert_awaited_once()

    session.list_tools.assert_awaited_once()


@pytest.mark.asyncio
async def test_execute_tool():
    client = MCPClient("server.py")

    session = AsyncMock()

    client.session = session

    content = MagicMock()

    content.text = "Project A"

    result = MagicMock()

    result.content = [content]

    session.call_tool.return_value = result

    output = await client.execute_tool(
        "list_projects",
        {},
    )

    assert output == "Project A"

    session.call_tool.assert_awaited_once_with(
        "list_projects",
        arguments={},
    )


@pytest.mark.asyncio
async def test_execute_tool_without_connection():
    client = MCPClient("server.py")

    with pytest.raises(RuntimeError):
        await client.execute_tool(
            "list_projects",
            {},
        )


@pytest.mark.asyncio
async def test_disconnect():
    client = MCPClient("server.py")

    client.exit_stack.aclose = AsyncMock()

    await client.disconnect()

    client.exit_stack.aclose.assert_awaited_once()