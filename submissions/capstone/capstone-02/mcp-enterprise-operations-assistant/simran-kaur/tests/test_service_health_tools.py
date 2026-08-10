import pytest
from servers.service_health_server import (list_services, get_service_health, get_active_incidents)


def test_list_services_returns_services():
    result = list_services()
    assert "services" in result.keys()
    assert result["count"] > 0
    for service in result["services"]:
        assert service["service_name"] is not None
        assert service["status"] is not None
     

def test_get_service_health_payment_api():

    input = "Payment API"
    result = get_service_health(input)

    assert result["found"] is True
    service = result["service"]
    assert service["service_name"] == "Payment API"
    assert service["status"] == "UNHEALTHY"
    assert service["error_rate_percent"] is not None
    assert service["average_latency_ms"] is not None


def test_get_service_health_unknown_service():
    input="Unknown Service"
    result=get_service_health(input)
    assert result["found"] == False
    assert result["message"] is not None


def test_get_active_incidents_payment_api():
    result = get_active_incidents('Payment API')
    assert result["count"] >= 1
    incidents = result["incidents"]
    for incident in incidents:
        assert incident["incident_id"]=="INC-OPS-101"
        assert incident["status"] == "ACTIVE"
    




