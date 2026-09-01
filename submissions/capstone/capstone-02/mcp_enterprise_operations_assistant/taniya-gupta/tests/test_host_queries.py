import os
import sys
import pytest
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPClient
from src.config import config
from src.host import run_query

sys.path.append(str(Path(__file__).resolve().parent.parent))

@pytest.fixture(scope='module')
def setup_env():
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        pytest.skip("Groq api key is not set")

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_payment_api_change_query(setup_env):
    client=MCPClient(config)
    llm=ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model=os.getenv("GROQ_MODEL"),
        temperature=0
    )
    try:
        await client.create_all_sessions()
        query="Why is the Payment API unhealthy and is there any recent change that may be related?"
        nl_response, servers_used, tools_used, evidence, structured= await run_query(llm, client, query)
        nl_lower=nl_response.lower()
        assert "payment api" in nl_lower
        assert "unhealthy" in nl_lower
        assert "error rate" in nl_lower
    finally:
        await client.close_all_sessions()

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_ticket_service_health_query(setup_env):
    client=MCPClient(config)
    llm=ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model=os.getenv("GROQ_MODEL"),
        temperature=0
    )
    try:
        await client.create_all_sessions()
        query="Show details of ticket TKT-1001 and check the heath of its related services "
        nl_response, servers_used, tools_used, evidence, structured= await run_query(llm, client, query)
        nl_lower=nl_response.lower()
        assert "tkt-1001" in nl_lower
        assert "payment api" in nl_lower
        assert "unhealthy" in nl_lower
    finally:
        await client.close_all_sessions()

@pytest.mark.integration
@pytest.mark.asyncio
async def test_multi_server_operations_summary(setup_env):
    client=MCPClient(config)
    llm=ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model=os.getenv("GROQ_MODEL"),
        temperature=0
    )
    try:
        await client.create_all_sessions()
        query="Give me operations summary of all unhealthy services, active incidents and high priority incidents "
        nl_response, servers_used, tools_used, evidence, structured= await run_query(llm, client, query)
        nl_lower=nl_response.lower()
        assert "payment api" in nl_lower
        assert "unhealthy" in nl_lower
        assert "inc-ops-101" in nl_lower
    finally:
        await client.close_all_sessions()


