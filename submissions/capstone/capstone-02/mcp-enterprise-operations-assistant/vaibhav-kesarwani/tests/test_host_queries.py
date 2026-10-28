import os
import pytest
from mcp_use import MCPClient, MCPAgent
from src.config import llm
from src.prompts import agent_system_prompt, JSON_SCHEMA_PROMPT

agent = None 

try:
    config = MCPClient("./src/mcp.json")
except Exception as e:
    pytest.fail(f"Not able to load the mcp.json file: {e}")

try:
    agent = MCPAgent(
        llm=llm,
        client=config,
        max_steps=10,
        use_server_manager=False,
        system_prompt=agent_system_prompt + "\n" + JSON_SCHEMA_PROMPT
    )
except Exception as e:
    pytest.fail(f"Error connecting with the agent: {e}")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_host_payment_api_change_query():
    query = "Why is the Payment API unhealthy and is there any recent change that may be related?"
    result = await agent.run(query)
    assert result


@pytest.mark.asyncio
@pytest.mark.integration
async def test_host_ticket_service_health_query():
    query = "Show the details of ticket TKT-1001 and check the health of its related service."
    result = await agent.run(query)
    assert result
