import pytest
from servers.service_health_server import list_services, load_service_health, get_service_health, get_active_incidents

data = load_service_health()

def test_list_services_returns_services():
    services = list_services()

    services_count = services["count"]
    services_list = services["services"]
    s_name_cnt = 0
    s_status_cnt = 0

    for service in services_list:
        if service["service_name"]:
            s_name_cnt += 1

        if service["status"]:
            s_status_cnt += 1

    assert services_list == data["services"]
    assert services_count >= 0
    assert s_name_cnt == len(data["services"])
    assert s_status_cnt == len(data["services"])


def test_get_service_health_payment_api(service_name: str= "Payment API"):
    data = get_service_health(service_name=service_name)

    found = data["found"]
    service = data["service"]

    assert found == True
    assert service["service_name"] == service_name
    assert service["status"] == "UNHEALTHY"
    assert service["error_rate_percent"] 
    assert service["average_latency_ms"]


def test_get_service_health_unknown_service(service_name: str= "Unknown Service"):
    data = get_service_health(service_name=service_name)

    found = data["found"]
    message = data["message"]

    assert found == False
    assert message


def test_get_active_incidents_payment_api(service_name: str= "Payment API"):
    data = get_active_incidents(service_name=service_name)

    count = data["count"]
    incident = data["incidents"]

    assert count >= 1
    assert incident[0]["status"] == "ACTIVE"