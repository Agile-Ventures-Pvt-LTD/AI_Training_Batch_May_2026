import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from servers.service_health_server import list_services, get_service_health, get_active_incidents


def test_list_services_returns_services():
    res = list_services()
    assert "services" in res
    assert res["count"] > 0
    for s in res["services"]:
        assert "service_name" in s
        assert "status" in s


def test_get_service_health_payment_api():
    res = get_service_health("Payment API")
    assert res["found"] is True
    assert res["service"]["service_name"] == "Payment API"
    assert "error_rate_percent" in res["service"]
    assert "average_latency_ms" in res["service"]


def test_get_service_health_unknown_service():
    res = get_service_health("NonExistentServiceXYZ")
    assert res["found"] is False
    assert "message" in res


def test_get_active_incidents_payment_api():
    res = get_active_incidents("Payment API")
    assert res["count"] > 0
    assert any(inc["incident_id"] == "INC-OPS-101" for inc in res["incidents"])