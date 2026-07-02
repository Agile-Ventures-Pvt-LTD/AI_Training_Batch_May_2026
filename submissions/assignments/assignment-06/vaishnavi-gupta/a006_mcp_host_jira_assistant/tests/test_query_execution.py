import pytest
from src.mcp_client import JiraMCPClient


@pytest.mark.asyncio
async def test_query_execution():
    """
    Verify that a Jira query executes successfully
    through the MCP server.
    """

    client = JiraMCPClient()

    try:
        await client.connect()

        result = await client.call_tool(
            "list_projects",
            {}
        )

        assert result is not None

        assert hasattr(result, "content")

        assert result is not None
        assert result.isError is False

    finally:
        await client.disconnect()
