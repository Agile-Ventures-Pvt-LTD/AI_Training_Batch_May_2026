
from servers.support_ticket_server import (search_ticket, get_ticket_details)
import pytest

def test_search_open_payment_tickets():
    service_name = "Payment API"
    status = "OPEN"
    result = search_ticket(service_name,status)
    tickets = result["tickets"]
    for ticket in tickets:
        assert ticket["service_name"]=="Payment API"
        assert ticket["status"]=="OPEN"
        assert result is not None


def test_get_ticket_details_valid_ticket():
    input="TKT-1001"

    result= get_ticket_details(input)

    assert result["found"] == True

    ticket= result["ticket"]

    assert ticket["ticket_id"] == "TKT-1001"
    assert ticket["service_name"] == "Payment API"
    assert ticket["priority"] is not None



def test_get_ticket_details_invalid_ticket():
    input="TKT-9999"
    result= get_ticket_details(input)
    assert result["found"] == False
    assert result["message"] is not None



# def test_high_priority_tickets_only_returns_p1_p2():

# priority is P1 or P2
# status is OPEN
