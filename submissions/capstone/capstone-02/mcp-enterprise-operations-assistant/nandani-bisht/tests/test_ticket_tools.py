from servers.support_ticket_server import search_tickets, get_ticket_details, get_high_priority_tickets

def test_search_open_payment_tickets():
    """Test search_tickets with filters on service and status."""
    result = search_tickets(service_name="Payment API", status="OPEN")
    assert "tickets" in result
    assert result["count"] > 0
    for ticket in result["tickets"]:
        assert ticket["service_name"] == "Payment API"
        assert ticket["status"] == "OPEN"
        assert "ticket_id" in ticket
        assert "priority" in ticket

def test_get_ticket_details_valid_ticket():
    """Test get_ticket_details returns correct data for a valid ticket."""
    result = get_ticket_details("TKT-1001")
    assert result["found"] is True
    ticket = result["ticket"]
    assert ticket["ticket_id"] == "TKT-1001"
    assert ticket["service_name"] == "Payment API"
    assert "priority" in ticket

def test_get_ticket_details_invalid_ticket():
    """Test get_ticket_details handles non-existent tickets gracefully."""
    result = get_ticket_details("TKT-9999")
    assert result["found"] is False
    assert "message" in result
    assert "Ticket not found." in result["message"]

def test_high_priority_tickets_only_returns_p1_p2():
    """Test get_high_priority_tickets returns only open P1 and P2 tickets."""
    result = get_high_priority_tickets()
    assert "tickets" in result
    assert result["count"] > 0
    for ticket in result["tickets"]:
        assert ticket["priority"] in ("P1", "P2")
        assert ticket["status"] == "OPEN"
