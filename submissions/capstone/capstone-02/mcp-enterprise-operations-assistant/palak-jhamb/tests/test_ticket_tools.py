from servers.support_ticket_server import search_tickets, get_high_priority_tickets,get_ticket_details

#Test 5 – Search Tickets
def test_search_open_payment_tickets():
    data=search_tickets(service_name = "Payment API",status = "OPEN")
    i=0
    while i in data:
        assert data["tickets"][i]["service_name"] =="Payment API"
        assert data["tickets"][i]["status"] =="OPEN"
        i+=1

# Test 6 – Ticket Details
def test_get_ticket_details_valid_ticket():
    data=get_ticket_details("TKT-1001")
    assert data["found"]==True
    assert data["ticket"]["ticket_id"]=="TKT-1001"
    assert data["ticket"]["service_name"]=="Payment API"
    assert "priority" in data["ticket"]


# Test 7 – Invalid Ticket
def test_get_ticket_details_invalid_ticket():
    data=get_ticket_details("TKT-9999")
    assert data["found"]==False
    assert "message" in data


# Test 8 – High-Priority Tickets
def test_high_priority_tickets_only_returns_p1_p2():
    data=get_high_priority_tickets()
    i=0
    while i in data:
        assert data["tickets"][i]["priority"] =="P1" or data["tickets"][i]["priority"] =="P2"
        assert data["tickets"][i]["status"] =="OPEN"
        i+=1
