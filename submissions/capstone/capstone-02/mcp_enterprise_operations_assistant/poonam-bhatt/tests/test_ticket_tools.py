import pytest
from src.tool_discovery import search_tickets, get_ticket_details, get_high_priority_tickets

def test_search_open_payment_tickets():
    """Test 5 - Search Tickets: Search open tickets for Payment API."""
    result = search_tickets(service_name="Payment API", status="OPEN")
    assert "tickets" in result
    assert result["count"] > 0
    for t in result["tickets"]:
        assert t["service_name"] == "Payment API"
        assert t["status"] == "OPEN"
        assert "ticket_id" in t
        assert "subject" in t

def test_get_ticket_details_valid_ticket():
    """Test 6 - Ticket Details: Get details for TKT-1001."""
    result = get_ticket_details("TKT-1001")
    assert result["found"] is True
    assert "ticket" in result
    ticket = result["ticket"]
    assert ticket["ticket_id"] == "TKT-1001"
    assert ticket["service_name"] == "Payment API"
    assert "priority" in ticket

def test_get_ticket_details_invalid_ticket():
    """Test 7 - Invalid Ticket: Get details for non-existent TKT-9999."""
    result = get_ticket_details("TKT-9999")
    assert result["found"] is False
    assert "message" in result

def test_high_priority_tickets_only_returns_p1_p2():
    """Test 8 - High-Priority Tickets: Verify only open P1 or P2 are returned."""
    result = get_high_priority_tickets()
    assert "tickets" in result
    for t in result["tickets"]:
        assert t["status"] == "OPEN"
        assert t["priority"] in ["P1", "P2"]
