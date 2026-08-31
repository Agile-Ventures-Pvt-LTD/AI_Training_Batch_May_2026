import pytest
import asyncio
import sys
from pathlib import Path

# sys.path.insert(0, str(Path(__file__).parent.parent))
from src.host import OperationsHost

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_payment_api_change_query():
    host = OperationsHost()
    query = "Why is the Payment API unhealthy and is there any recent change that may be related?"
    result = await host.process_query(query)
    await host.close()
    
    assert result["status"] == "PASS"
    summary = result.get("operations_summary", "").lower()
    assert "payment api" in summary
    assert "unhealthy" in summary
    assert "inc-ops-101" in summary or "incident" in summary
    assert "chg-2001" in summary or "change" in summary
    correlation = result.get("possible_change_correlation", "").lower()
    assert "confirmed root cause" not in correlation

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_ticket_service_health_query():
    host = OperationsHost()
    query = "Show the details of ticket TKT-1001 and check the health of its related service."
    result = await host.process_query(query)
    await host.close()
    
    assert result["status"] == "PASS"
    summary = result.get("operations_summary", "").lower()
    assert "tkt-1001" in summary
    assert "payment api" in summary
    assert "unhealthy" in summary

@pytest.mark.integration
@pytest.mark.asyncio
async def test_host_multi_server_operations_summary():
    host = OperationsHost()
    query = "Give me an operations summary of all unhealthy or degraded services, active incidents, and high-priority tickets."
    result = await host.process_query(query)
    await host.close()
    
    assert result["status"] == "PASS"
    assert "service-health" in result.get("servers_used", [])
    assert "support-ticket" in result.get("servers_used", [])
