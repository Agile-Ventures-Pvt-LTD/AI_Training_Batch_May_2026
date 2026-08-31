import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from servers.support_ticket_server import search_tickets, get_ticket_details, get_high_priority_tickets

def test_search_open_payment_tickets():
    result = search_tickets(service_name="Payment API", status="OPEN")
    assert result["count"] > 0
    for t in result["tickets"]:
        assert t["service_name"] == "Payment API"
        assert t["status"] == "OPEN"

def test_get_ticket_details_valid_ticket():
    result = get_ticket_details(ticket_id="TKT-1001")
    assert result["found"] is True
    assert result["ticket"]["ticket_id"] == "TKT-1001"
    assert result["ticket"]["service_name"] == "Payment API"
    assert "priority" in result["ticket"]

def test_get_ticket_details_invalid_ticket():
    result = get_ticket_details(ticket_id="TKT-9999")
    assert result["found"] is False
    assert "message" in result

def test_high_priority_tickets_only_returns_p1_p2():
    result = get_high_priority_tickets()
    for t in result["tickets"]:
        assert t["priority"] in ["P1", "P2"]
        assert t["status"] == "OPEN"

