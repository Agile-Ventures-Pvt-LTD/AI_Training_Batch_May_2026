import asyncio
import pytest

from src.agent import Agent

@pytest.mark.asyncio
async def test_mcp_agent_runs():
    """
    Verify that the agent runs successfully.
    """

    client = Agent()

    try:
        await client.connect()

        assert client.session is not None
        
    finally:
        await client.disconnect()
