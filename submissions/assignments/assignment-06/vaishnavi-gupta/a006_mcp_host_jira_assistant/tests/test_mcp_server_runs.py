import asyncio
import pytest

from src.mcp_client import JiraMCPClient


@pytest.mark.asyncio
async def test_mcp_server_runs():
    """
    Verify that the MCP server starts successfully.
    """

    client = JiraMCPClient()

    try:
        await client.connect()

        assert client.session is not None
        
    finally:
        await client.disconnect()
