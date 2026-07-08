import pytest 
from src.host import agent
@pytest.mark.integration
@pytest.mark.asyncio 
async def test_host_payment_api_change_query(): 
    answer = await agent( "Why is the Payment API unhealthy and is there any recent change that may be related?" ) 
    assert "Payment API" in answer 
    assert "unhealthy" in answer.lower() 
    assert "incident" in answer.lower() 
    assert "change" in answer.lower() 
@pytest.mark.integration 
@pytest.mark.asyncio 
async def test_host_ticket_service_health_query(): 
    answer = await agent( "Show the details of ticket TKT-1001 and check the health of its related service." ) 
    assert "TKT-1001" in answer
    assert "Payment API" in answer