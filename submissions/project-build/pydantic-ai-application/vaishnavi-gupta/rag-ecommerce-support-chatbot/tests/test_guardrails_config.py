import asyncio
import pytest

from src.guardrails_config import Guard


@pytest.mark.asyncio
async def test_guardrails_config_runs():
    """
    Verify that the MCP server starts successfully.
    """

    client = Guard()

    try:
        await client.connect()

        assert client.session is not None
        
    finally:
        await client.disconnect()
