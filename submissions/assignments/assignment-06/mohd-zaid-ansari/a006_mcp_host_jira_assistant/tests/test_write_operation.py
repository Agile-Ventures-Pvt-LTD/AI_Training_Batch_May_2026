import pytest
from src.llm import get_llm
from src.mcp_client import mcp_client
from mcp_use import MCPAgent

@pytest.mark.asyncio
async def test_multi_flow():
    agent = MCPAgent(
        llm=get_llm(),
        client=mcp_client(),
    )
    agent.tools_used_names.clear()
    await agent.run("Add comments to MCP-3 saying testing dashboard")
    assert "add_issue_comment" in agent.tools_used_names