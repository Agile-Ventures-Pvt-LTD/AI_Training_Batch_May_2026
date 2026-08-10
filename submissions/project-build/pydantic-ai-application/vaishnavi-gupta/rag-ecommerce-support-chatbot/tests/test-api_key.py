import asyncio
import pytest

from src.env import GROQ_API_KEY


@pytest.mark.asyncio
async def test_api_runs():
    """
    Verify that the MCP server starts successfully.
    """

    client = GROQ_API_KEY()

    try:
        await client.connect()

        assert client.session is not None
        
    finally:
        await client.disconnect()
