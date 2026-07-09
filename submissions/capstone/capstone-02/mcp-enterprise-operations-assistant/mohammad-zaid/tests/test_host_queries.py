import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.host import handle_operations_query, StructuredOpsResponse


@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_payment_api_change_query():
    query = "Why is the Payment API unhealthy and is there any recent change that may be related?"
    res = await handle_operations_query(query, query_id="TEST_Q1")
    
    assert isinstance(res, StructuredOpsResponse)
    assert res.user_query == query
    assert "service-health" in res.servers_used
    assert "change-management" in res.servers_used
    assert len(res.evidence.services) > 0
    assert "Payment API" in res.operations_summary


@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_ticket_service_health_query():
    query = "Show the details of ticket TKT-1001 and check the health of its related service."
    res = await handle_operations_query(query, query_id="TEST_Q7")
    
    assert isinstance(res, StructuredOpsResponse)
    assert "service-health" in res.servers_used
    assert res.evidence.tickets is not None