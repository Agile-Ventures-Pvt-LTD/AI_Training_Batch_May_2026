import pytest
from src.tool_discovery import list_services, get_service_health, get_active_incidents

def test_list_services_returns_services():
    """Test 1 - List Services: Validate returned list structure."""
    result = list_services()
    assert "services" in result
    assert "count" in result
    assert result["count"] > 0
    for s in result["services"]:
        assert "service_name" in s
        assert "status" in s
        assert "region" in s

def test_get_service_health_payment_api():
    """Test 2 - Valid Service Health: Check details for Payment API."""
    result = get_service_health("Payment API")
    assert result["found"] is True
    assert "service" in result
    service = result["service"]
    assert service["service_name"] == "Payment API"
    assert service["status"] == "UNHEALTHY"
    assert "error_rate_percent" in service
    assert "average_latency_ms" in service

def test_get_service_health_unknown_service():
    """Test 3 - Invalid Service: Check response for non-existent service."""
    result = get_service_health("Unknown Service")
    assert result["found"] is False
    assert "message" in result

def test_get_active_incidents_payment_api():
    """Test 4 - Active Incidents: Check active incidents for Payment API."""
    result = get_active_incidents("Payment API")
    assert "incidents" in result
    assert result["count"] >= 1
    
    incident_ids = [inc["incident_id"] for inc in result["incidents"]]
    assert "INC-OPS-101" in incident_ids
    
    for inc in result["incidents"]:
        assert inc["status"] == "ACTIVE"
        assert inc["service_name"] == "Payment API"
