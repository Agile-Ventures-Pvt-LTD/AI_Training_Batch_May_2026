import pytest
import asyncio
from servers.service_health_server import list_services, get_service_health, get_active_incident
from servers.support_ticket_server import search_tickets, get_ticket_details, get_high_priority_tickets
from servers.change_management_server import list_recent_changes, get_change_details, get_changes_for_service

@pytest.mark.asyncio
async def test_mcp_server_runs():
    """
    Verify that the MCP server starts successfully.
    """

    client = MCPClient()

    try:
        await client.connect()

        assert client.session is not None
        
    finally:
        await client.disconnect()

@pytest.mark.asyncio
def test_get_changes_for_payment_api():
    if service_name == "Payment API":
        print("Valid")


@pytest.mark.asyncio
def test_get_change_details_valid_change():
    if (found == True && change_id == "CHG-2001" && service_name == "Payment API):
        print("Valid")

