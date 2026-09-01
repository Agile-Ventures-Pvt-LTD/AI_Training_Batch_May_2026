import sys
from pathlib import Path
from servers.service_health_server import get_service_health, list_services, get_active_incidents

sys.path.append(str(Path(__file__).resolve().parent.parent))

def test_list_services_returns_services():
    result=list_services()
    assert "services" in result
    for s in result["services"]:
        assert "service_name" in s
        assert "status" in s

def test_get_service_health_payment_api():
    result=get_service_health("Payment API")
    assert result["found"] is True
    service=result["service"]
    assert service["service_name"]=="Payment API"
    assert service["status"]=="UNHEALTHY"

def test_get_service_unknown_service():
    result=get_service_health("Unknown service")
    assert result["found"] is False
    assert "msg" in result

def test_get_active_incidents_payment_api():
    result=get_active_incidents("Payment API")
    assert "incidents" in result
    incident_id=[inc["incident_id"] for inc in result["incidents"]]
    assert "INC-OPS-101" in incident_id
    for inc in result["incidents"]:
        assert inc["status"]=="ACTIVE"
        