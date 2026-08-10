from servers.service_health_server import ( list_services, get_service_health, get_active_incidents, ) 
def test_list_services_returns_services(): 
    result = list_services() 
    assert result["count"] > 0 
    assert "services" in result 
    assert "service_name" in result["services"][0]
    assert "status" in result["services"][0] 
def test_get_service_health_payment_api(): 
    result = get_service_health("Payment API") 
    assert result["found"] is True 
    assert result["service"]["service_name"] == "Payment API" 
    assert result["service"]["status"] == "UNHEALTHY" 
    assert "error_rate_percent" in result["service"] 
    assert "average_latency_ms" in result["service"] 
def test_get_service_health_unknown_service(): 
    result = get_service_health("Unknown Service") 
    assert result["found"] is False 
    assert "message" in result 
def test_get_active_incidents_payment_api():
     result = get_active_incidents("Payment API") 
     assert result["count"] >= 1 
     assert any( incident["incident_id"] == "INC-OPS-101" for incident in result["incidents"] ) 
     assert all( incident["status"] == "ACTIVE" for incident in result["incidents"] )