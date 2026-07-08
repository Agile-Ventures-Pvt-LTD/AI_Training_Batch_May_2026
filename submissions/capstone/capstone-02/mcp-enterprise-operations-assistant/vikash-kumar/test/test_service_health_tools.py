import json
import pytest
from servers.service_health_server import list_services, get_service_health, get_active_incidents

def test_list_services():
    result = json.loads(list_services())
    assert "count" in result
    assert "services" in result

def test_get_service_health_valid():
    result = json.loads(get_service_health("payment-gateway"))
    assert result["found"] is True
    assert "service" in result

def test_get_service_health_invalid():
    result = json.loads(get_service_health("non-existent-service"))
    assert result["found"] is False

def test_get_active_incidents_all():
    result = json.loads(get_active_incidents())
    assert "count" in result
    assert "incidents" in result
