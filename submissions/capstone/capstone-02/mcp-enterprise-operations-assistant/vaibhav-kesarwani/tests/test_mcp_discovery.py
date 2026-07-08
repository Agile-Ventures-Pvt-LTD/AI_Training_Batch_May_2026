import json
import pytest
import asyncio
from src.tool_discovery import fetch_tools

MCP_FILE = "./src/mcp.json"

@pytest.mark.asyncio
async def test_mcp_discovery():
    with open(MCP_FILE, "r") as f:
        data = json.load(f)
        
    assert "mcpServers" in data and isinstance(data["mcpServers"], dict)

    tasks = [
        fetch_tools(server_name, server_info)
        for server_name, server_info in data["mcpServers"].items()
    ]

    results = await asyncio.gather(*tasks)

    assert results
    assert all(result is not None for result in results)
