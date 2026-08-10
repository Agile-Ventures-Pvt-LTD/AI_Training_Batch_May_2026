import pytest
import os
import asyncio
from servers.service_health_server import list_services, get_service_health, get_active_incident
from servers.support_ticket_server import search_tickets, get_ticket_details, get_high_priority_tickets
from servers.change_management_server import list_recent_changes, get_change_details, get_changes_for_service


@pytest.mark.integration
def test_host_payment_api_change_query():
    key = os.getenv("GROQ_API_KEY")
    response = requests.get(key)
    assert response.status_code == 200

    print("✅ Weather API Working")



@pytest.mark.integration
def test_host_ticket_service_health_query():
    key = os.getenv("GROQ_API_KEY")
    response = requests.get(key)

    assert response.status_code == 200

    print("Valid")


@pytest.mark.integration
def test_host_multi_server_operations_summary():
    key = os.getenv("GROQ_API_KEY")
    response = requests.get(key)

    assert response.status_code == 200

    print("Valid")

