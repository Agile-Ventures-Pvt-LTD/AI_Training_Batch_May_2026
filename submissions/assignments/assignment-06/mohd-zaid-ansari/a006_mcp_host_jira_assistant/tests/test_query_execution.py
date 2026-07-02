import pytest
from src.llm import get_llm
from src.mcp_client import mcp_client
from mcp_use import MCPAgent

@pytest.mark.asyncio
async def test_query_execution():
    agent = MCPAgent(
        llm=get_llm(),
        client=mcp_client(),
    )
    response = await agent.run("List all Jira projects.")
    assert response is not None
    assert len(str(response)) > 0