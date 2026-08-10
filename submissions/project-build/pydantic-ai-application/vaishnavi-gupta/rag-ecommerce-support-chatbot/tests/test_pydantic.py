import asyncio
import pytest

from src.agent import Agent


@pytest.mark.asyncio
async def test_pydantic_runs():
    """
    Verify that the MCP server starts successfully.
    """

    client = Agent()

    try:
        await client.connect()

        assert client.session is not None
        
    finally:
        await client.disconnect()
