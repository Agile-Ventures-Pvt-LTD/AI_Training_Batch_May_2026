import json
import pytest
from servers.support_ticket_server import search_tickets, get_ticket_details, get_high_priority_tickets

def test_search_tickets_all():
    result = json.loads(search_tickets(limit=5))
    assert "count" in result
    assert "tickets" in result

def test_get_ticket_details_valid():
    result = json.loads(get_ticket_details("TKT-1"))
    assert result["found"] is True
    assert "ticket" in result

def test_get_high_priority_tickets():
    result = json.loads(get_high_priority_tickets())
    assert "count" in result
    assert "tickets" in result
