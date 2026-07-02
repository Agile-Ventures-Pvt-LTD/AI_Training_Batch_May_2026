import pytest
from pathlib import Path
from fastmcp import Client

PROJECT_ROOT=Path(__file__).resolve().parent.parent
SERVER_PATH=PROJECT_ROOT/ "server" / "jira_mcp_server.py"

@pytest.mark.asyncio
async def test_mcp_server():
    client=Client(SERVER_PATH)
    async with client:
        assert client is not None
    await client.close()
