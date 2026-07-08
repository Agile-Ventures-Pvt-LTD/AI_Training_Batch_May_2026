import os
import pytest
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from src.config import MCP_CONFIG
from src.prompts import system_prompt
from src.host import OperationsResponse

# Load environment variables
load_dotenv()

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_payment_api_change_query():
    """Test 12 - Integration Test: Payment API and Change."""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        pytest.skip("GROQ_API_KEY not found in environment")
        
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=0,
        api_key=groq_api_key
    )
    client = MCPClient(MCP_CONFIG)
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        system_prompt=system_prompt
    )
    
    try:
        await client.create_all_sessions()
        query = "Why is the Payment API unhealthy and is there any recent change that may be related?"
        response = await agent.run(query, output_schema=OperationsResponse)
        
        # Validation checks
        assert response.user_query == query
        assert any(s in response.servers_used for s in ["service-health", "service_health"])
        assert any(s in response.servers_used for s in ["change-management", "change_management"])
        
        text = response.operations_summary.lower()
        assert "payment" in text
        
        # Correlation speculation check
        correlation = response.possible_change_correlation.lower()
        assert "cause" not in correlation or "indicates" in correlation or "may" in correlation or "possible" in correlation or "suggests" in correlation
        
    finally:
        await client.close_all_sessions()

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_ticket_service_health_query():
    """Test 13 - Integration Test: Ticket and Service Health."""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        pytest.skip("GROQ_API_KEY not found in environment")
        
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=0,
        api_key=groq_api_key
    )
    client = MCPClient(MCP_CONFIG)
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        system_prompt=system_prompt
    )
    
    try:
        await client.create_all_sessions()
        query = "Show the details of ticket TKT-1001 and check the health of its related service."
        response = await agent.run(query, output_schema=OperationsResponse)
        
        # Validation checks
        assert any(s in response.servers_used for s in ["support-ticket", "support_ticket"])
        assert any(s in response.servers_used for s in ["service-health", "service_health"])
        
        summary = response.operations_summary
        assert "TKT-1001" in summary
        assert "Payment API" in summary
        
    finally:
        await client.close_all_sessions()

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_multi_server_operations_summary():
    """Test 14 - Integration Test: Operations summary of all unhealthy services, incidents, and tickets."""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        pytest.skip("GROQ_API_KEY not found in environment")
        
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=0,
        api_key=groq_api_key
    )
    client = MCPClient(MCP_CONFIG)
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        system_prompt=system_prompt
    )
    
    try:
        await client.create_all_sessions()
        query = "Give me an operations summary of all unhealthy or degraded services, active incidents, and high-priority tickets."
        response = await agent.run(query, output_schema=OperationsResponse)
        
        assert any(s in response.servers_used for s in ["service-health", "service_health"])
        assert any(s in response.servers_used for s in ["support-ticket", "support_ticket"])
        
        summary = response.operations_summary.lower()
        assert "unhealthy" in summary or "degraded" in summary or "payment" in summary or "checkout" in summary
        
    finally:
        await client.close_all_sessions()
