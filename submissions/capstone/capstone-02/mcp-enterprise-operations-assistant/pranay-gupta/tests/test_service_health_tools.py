from servers.service_health_server import list_services,get_service_health,get_active_incidents
import pytest

def test_list_services_returns_services():
    result = list_services()
    assert "count" in result
    assert result["count"]>0
    assert "services" in result
    for s in result["services"]:
        assert "service_name" in s
        assert "status" in s

def test_get_service_health_payment_api():
    result = get_service_health(service_name="Payment API")
    assert result["found"] is True
    assert result["service"]["service_name"] == "Payment API"
    assert result["service"]["status"] == "UNHEALTHY"
    assert "error_rate_percent" in result["service"]
    assert "average_latency_ms" in result["service"]

def test_get_service_health_unknown_service():
    result = get_service_health(service_name="Unknown Service")
    assert result["found"] is False
    assert "message" in result

def test_get_active_incidents_payment_api():
    result = get_active_incidents(service_name="Payment API")
    assert result["count"] >= 1
    incident_ids = [inc["incident_id"] for inc in result["incidents"]]
    assert "INC-OPS-101" in incident_ids
    assert all(inc["status"] == "ACTIVE" for inc in result["incidents"])