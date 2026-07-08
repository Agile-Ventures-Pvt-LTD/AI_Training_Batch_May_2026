import pytest
from src.host import run_single_query

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_payment_api_change_query():
    """Verify Q1 end-to-end execution, checking tool calls and output content."""
    query = "Why is the Payment API unhealthy and is there any recent change that may be related?"
    result = await run_single_query(query)
    
    
    summary = result.get("operations_summary", "").lower()
    correlation = result.get("possible_change_correlation", "").lower()
    
    assert "payment api" in summary
    assert "unhealthy" in summary or "error rate" in summary
    assert "incident" in summary or "inc-ops-101" in summary
    
   
    assert "definitely caused" not in summary
    assert "definitely caused" not in correlation
    
    
    tools_used = result.get("tools_used", [])
    servers_used = result.get("servers_used", [])
    
    assert "service-health" in servers_used
    assert "change-management" in servers_used

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_ticket_service_health_query():
    """Verify Q7 end-to-end execution, ensuring details of TKT-1001 and related service health are pulled."""
    query = "Show the details of ticket TKT-1001 and check the health of its related service."
    result = await run_single_query(query)
    
    summary = result.get("operations_summary", "").lower()
    
    assert "tkt-1001" in summary
    assert "payment api" in summary
    assert "unhealthy" in summary or "error rate" in summary

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_multi_server_operations_summary():
    """Verify Q5 end-to-end execution, summarizing unhealthy services and tickets across servers."""
    query = "Give me an operations summary of all unhealthy or degraded services, active incidents, and high-priority tickets."
    result = await run_single_query(query)
    
    summary = result.get("operations_summary", "").lower()
    
    assert "payment api" in summary
    assert "checkout service" in summary
    assert "incident" in summary
    assert "ticket" in summary or "tkt" in summary
