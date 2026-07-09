from servers.service_health_server import list_services, get_active_incidents,get_service_health

# Test 1 – List Services
def test_list_services_returns_services():
    data=list_services()
    assert data is not None
    assert data["count"]>0
    assert "service_name" in data["services"][0]
    assert "status" in data["services"][0]

# Test 2 – Valid Service Health
def test_get_service_health_payment_api():
    data=get_service_health("Payment API")
    assert data["found"]==True
    assert data["service"]["service_name"]=="Payment API"
    assert data["service"]["status"]=="UNHEALTHY"
    assert "error_rate_percent" in data["service"]
    assert "average_latency_ms" in data["service"]


# Test 3 – Invalid Service
def test_get_service_health_unknown_service():
    data=get_service_health("Unknown Service")
    assert data["found"]==False
    assert "message" in data

# Test 4 – Active Incidents
def test_get_active_incidents_payment_api():
    data=get_active_incidents("Payment API")
    assert "INC-OPS-101" in data["incidents"][0]["incident_id"]
    assert data["incidents"][0]["status"]=="ACTIVE"


