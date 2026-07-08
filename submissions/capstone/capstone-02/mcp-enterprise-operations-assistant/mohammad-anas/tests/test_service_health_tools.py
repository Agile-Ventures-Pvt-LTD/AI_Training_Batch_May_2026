import pytest
from servers.service_health_server import list_services,get_service_health,get_active_incidents

def test_list_service_returns_service():
    result = list_services()
    assert "service" in result
    assert result["count"] > 0
    assert "service_name" in result["services[0]"]
    assert "status" in result["service"][0]
    
def test_get_active_incidents_payment_api():
    result = get_active_incidents("Payment API")
    assert result["count"] >= 1
    incident_ids = [inc["incident_id"] for inc in result["incidents"]]
    assert "INC-OPS-101" in incident_ids
    for inc in result["incidents"]:
        assert inc["status"] == "ACTIVE"