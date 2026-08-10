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
    await agent.run("Which issues are assigned to Mohd Zaid Ansari.")
    assert len(agent.tools_used_names)>=2