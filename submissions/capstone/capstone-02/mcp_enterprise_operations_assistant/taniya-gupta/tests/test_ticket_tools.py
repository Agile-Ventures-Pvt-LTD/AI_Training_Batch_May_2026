import sys
from pathlib import Path
from servers.support_ticket_server import get_ticket_details,search_tickets,get_high_priority_tickets

sys.path.append(str(Path(__file__).resolve().parent.parent))

def test_get_open_payment_tickets():
    result=search_tickets(service_name="Payment API", status="OPEN")
    assert "tickets" in result
    for t in result["tickets"]:
        assert t["service_name"]=="Payment API"
        assert t["status"]=="OPEN"

def test_get_tickets_details_valid_ticket():
    result=get_ticket_details("TKT-1001")
    assert result["found"] is True
    ticket=result["ticket"]
    assert ticket["ticket_id"]=="TKT-1001"
    assert ticket["service_name"]=="Payment API"
    assert "priority" in ticket

def test_high_priority_tickets_only_returns_p1_p2():
    result=get_high_priority_tickets()
    assert "tickets" in result
    for t in result["tickets"]:
        assert t["priority"] in ["P1", "P2"]
        assert t["status"] == "OPEN"