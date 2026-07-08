import pytest
from src.host import MCPOperations

@pytest.mark.asyncio
async def test_orchestrator_execution_flow():
    agent = MCPOperations()
    result = agent.execute_workflow("Check performance metrics for payment-gateway")
    assert "query" in result
    assert "tool_used" in result
    assert "result" in result

@pytest.mark.asyncio
async def test_orchestrator_unmatched_query():
    agent = MCPOperations()
    result = agent.execute_workflow("check generic server check echo status")
    assert result["tool_used"] == "None"
