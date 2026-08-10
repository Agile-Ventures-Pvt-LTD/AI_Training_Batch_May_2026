import pytest
from servers.support_ticket_server import search_tickets, get_ticket_details, get_high_priority_tickets

@pytest.mark.asyncio
async def test_search_open_payment_tickets():
    result= await search_tickets("Payment API", "OPEN")

    assert result["count"]>=1
    assert "tickets" in result
    assert len(result["tickets"]) >= 1

    tickets={ticket.get("ticket_id") for ticket in result["tickets"]}
    assert "OPEN" in tickets

    for ticket in result["tickets"]:
        assert ticket.get("service_name") == "Payment API"
        assert ticket.get("status") == "OPEN"

#=================================================================================================================

@pytest.mark.asyncio
async def test_get_ticket_details_valid_ticket():
    result=await get_ticket_details("TKT-1001")

    assert result["Found"] is True
    assert "ticket" in result

    ticket=result["ticket_id"]
    assert ticket["found"] == True
    assert ticket["ticket_id"] == "TCT-1001"
    assert ticket["service_name"] == "Payment API"
    assert "Priority exists" in ticket

#==================================================================================================================

@pytest.mark.asyncio
async def test_get_ticket_details_invalid_ticket():
    result=await get_ticket_details("TKT-9999")

    assert result["Found"] is False
    assert "ticket" in result

    ticket=result["ticket_id"]
    assert ticket["found"] == False
    assert "Application does not crash" in ticket
    assert ticket["message"] == "Ticket not found"

#====================================================================================================================

@pytest.mark.asyncio
async def test_high_priority_tickets_only_returns_p1_p2():
    result= await get_high_priority_tickets("Payment API")

    assert result["Found"] is True
    assert "tickets" in result

    ticket=result["service_name"]
    assert ticket["service_name"] == "Payment API"
    assert ticket["Priority"] == 'P1'
    assert ticket["Status"] == "OPEN"

