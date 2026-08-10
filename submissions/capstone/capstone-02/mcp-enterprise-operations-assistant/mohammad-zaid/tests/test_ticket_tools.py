import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from servers.support_ticket_server import search_tickets, get_ticket_details, get_high_priority_tickets


def test_search_open_payment_tickets():
    res = search_tickets(service_name="Payment API", status="OPEN")
    assert "tickets" in res
    for ticket in res["tickets"]:
        assert ticket["service_name"] == "Payment API"
        assert ticket["status"] == "OPEN"


def test_get_ticket_details_valid_ticket():
    res = get_ticket_details("TKT-1001")
    assert res["found"] is True
    assert res["ticket"]["ticket_id"] == "TKT-1001"
    assert res["ticket"]["service_name"] == "Payment API"


def test_get_ticket_details_invalid_ticket():
    res = get_ticket_details("TKT-9999")
    assert res["found"] is False
    assert "message" in res


def test_high_priority_tickets_only_returns_p1_p2():
    res = get_high_priority_tickets()
    for ticket in res["tickets"]:
        assert ticket["priority"] in ["P1", "P2"]
        assert ticket["status"] == "OPEN"