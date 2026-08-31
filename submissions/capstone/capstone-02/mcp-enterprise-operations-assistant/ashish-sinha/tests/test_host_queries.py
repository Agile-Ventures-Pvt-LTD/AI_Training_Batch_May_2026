import pytest
from src.host import Hostrun

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_payment_api_change_query():
    query= 'Why is the Payment API unhealthy and is there any recent change that may be related?'
    answer = await Hostrun(query)
    assert 'Payment API' in answer
    assert 'unhealthy' in answer.lower()
    assert 'active' in answer.lower()
    assert 'change' in answer.lower()



@pytest.mark.integration
@pytest.mark.asyncio
async def  test_host_ticket_service():
    query = 'Show the details of ticket TKT-1001 and check the health of its related service.'
    answer = await Hostrun(query)
    assert 'TKT-1001' in answer
    assert 'Payment API' in answer
    assert 'healthy' in answer.lower() or 'unhealthy' in answer.lower()
