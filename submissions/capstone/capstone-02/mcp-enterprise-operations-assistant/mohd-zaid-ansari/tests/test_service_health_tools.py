import pytest

from servers.service_health_server import list_services,get_service_health,get_active_incidents

@pytest.mark.asyncio
async def test_list_services_returns_services():

    result = await list_services()

    assert "services" in result
    assert result["count"] > 0
    assert len(result["services"]) > 0

    for svc in result["services"]:
        assert "service_name" in svc
        assert svc["service_name"] is not None
        assert "status" in svc
        assert svc["status"] is not None

#=======================================================================================================================

@pytest.mark.asyncio
async def test_get_service_health_payment_api():

    result = await get_service_health("Payment API")

    assert result["found"] is True
    assert "service" in result

    svc = result["service"]
    assert svc["service_name"] == "Payment API"
    assert svc["status"] == "UNHEALTHY"
    assert "error_rate_percent" in svc
    assert "average_latency_ms" in svc

#=======================================================================================================================

@pytest.mark.asyncio
async def test_get_service_health_unknown_service():

    result = await get_service_health("Unknown Service")

    assert result["found"] is False
    assert "message" in result
    assert isinstance(result["message"], str)
    assert result["message"].strip() != ""

#========================================================================================================================

@pytest.mark.asyncio
async def test_get_active_incidents_payment_api():
    result = await get_active_incidents("Payment API")

    assert result["count"] >= 1
    assert "incidents" in result
    assert len(result["incidents"]) >= 1

    incident_ids = {inc.get("incident_id") for inc in result["incidents"]}
    assert "INC-OPS-101" in incident_ids

    for inc in result["incidents"]:
        assert inc.get("service_name") == "Payment API"
        assert inc.get("status") == "ACTIVE"

