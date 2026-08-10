import os
import pytest
from mcp_client import JiraMCPClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_SCRIPT = os.path.join(PROJECT_ROOT, "server", "jira_mcp_server.py")


@pytest.mark.asyncio
async def test_tool_discovery(expected_tool_names):
    client = JiraMCPClient(SERVER_SCRIPT)
    async with client:
        tools = await client.list_tools_for_groq()

    discovered = {t["function"]["name"] for t in tools}
    assert discovered == set(expected_tool_names)


@pytest.mark.asyncio
async def test_discovered_tools_are_valid_groq_function_schemas():
    client = JiraMCPClient(SERVER_SCRIPT)
    async with client:
        tools = await client.list_tools_for_groq()

    for tool in tools:
        assert tool["type"] == "function"
        assert "name" in tool["function"]
        assert "parameters" in tool["function"]
        assert isinstance(tool["function"]["parameters"], dict)


@pytest.mark.asyncio
async def test_write_tools_require_issue_key_argument():
    client = JiraMCPClient(SERVER_SCRIPT)
    async with client:
        tools = await client.list_tools_for_groq()

    by_name = {t["function"]["name"]: t for t in tools}
    for name in ("add_issue_comment", "update_issue_status"):
        params = by_name[name]["function"]["parameters"]
        assert "issue_key" in params.get("properties", {})
