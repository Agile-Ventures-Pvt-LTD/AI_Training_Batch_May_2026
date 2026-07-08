import pytest
from servers.support_ticket_server import get_high_priority_tickets,get_ticket_details,_get_connection

def test_search_open_payment_tickets (): 
    result = get_ticket_details()
    assert result["service_name"] == "Payment API" 
    assert result["status"] == "OPEN"
    
def test_get_ticket_details_valid_ticket(): 
    result = get_ticket_details("TKT-1001")
    assert result["found"] is True 
    assert result["ticket_id"]=="TKT-1001"
    assert result["service_name"] == "Payment API" 
    assert result['priority'] is False