from servers.service_health_server import list_services, get_service_health, get_active_incidents

def test_list_services_returns_services():
    """Test list_services returns the correct services and fields."""
    result = list_services()
    assert "services" in result
    assert result["count"] > 0
    for service in result["services"]:
        assert "service_name" in service
        assert "status" in service
        assert "region" in service

def test_get_service_health_payment_api():
    """Test get_service_health returns details for Payment API."""
    result = get_service_health("Payment API")
    assert result["found"] is True
    service = result["service"]
    assert service["service_name"] == "Payment API"
    assert service["status"] == "UNHEALTHY"
    assert "error_rate_percent" in service
    assert "average_latency_ms" in service

def test_get_service_health_unknown_service():
    """Test get_service_health returns appropriate error for invalid service."""
    result = get_service_health("Unknown Service")
    assert result["found"] is False
    assert "message" in result
    assert "Service not found." in result["message"]

def test_get_active_incidents_payment_api():
    """Test get_active_incidents returns active incident for Payment API."""
    result = get_active_incidents("Payment API")
    assert result["count"] >= 1
    incidents = result["incidents"]
    
    found_inc = False
    for inc in incidents:
        if inc["incident_id"] == "INC-OPS-101":
            found_inc = True
            assert inc["status"] == "ACTIVE"
            assert inc["service_name"] == "Payment API"
    assert found_inc is True
