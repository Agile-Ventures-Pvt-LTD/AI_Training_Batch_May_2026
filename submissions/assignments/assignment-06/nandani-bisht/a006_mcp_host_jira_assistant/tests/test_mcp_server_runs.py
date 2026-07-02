import os
import pytest
from mcp_client import JiraMCPClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_SCRIPT = os.path.join(PROJECT_ROOT, "server", "jira_mcp_server.py")


@pytest.mark.asyncio
async def test_mcp_server_runs():
    client = JiraMCPClient(SERVER_SCRIPT)
    async with client:
        tools = await client.list_tools_for_groq()
    assert isinstance(tools, list)
    assert len(tools) > 0


@pytest.mark.asyncio
async def test_mcp_server_can_be_entered_multiple_times_sequentially():
    for _ in range(2):
        client = JiraMCPClient(SERVER_SCRIPT)
        async with client:
            tools = await client.list_tools_for_groq()
        assert len(tools) == 6
