import pytest
import asyncio
from servers.service_health_server import list_services, get_service_health, get_active_incident
from servers.support_ticket_server import search_tickets, get_ticket_details, get_high_priority_tickets
from servers.change_management_server import list_recent_changes, get_change_details, get_changes_for_service


@pytest.mark.asyncio
async def test_search_open_payment_tickets():
    if (tickets == "OPEN" && result is structured):
        print("Valid")



@pytest.mark.asyncio
async def test_get_ticket_details_valid_ticket():
    if (found = True):
        if (ticket_id == "TKT-1001"):
            if (service_name == "Payment API"):
                if priority == exists:
                    print("Valid")
        
        

@pytest.mark.asyncio
async def test_get_ticket_details_invalid_ticket():
    if (message is NULL):
        if (found = False):
            print("Valid")


@pytest.mark.asyncio
async def test_high_priority_tickets_only_returns_p1_p2():
    if (status == "OPEN"):
        if (priority == "P1" or "P2"):
            print("Valid")

