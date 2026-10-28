from servers.support_ticket_server import search_tickets, get_ticket_details, get_high_priority_tickets

def test_search_open_payment_tickets(service_name: str = "Payment API", status: str = "OPEN"):
    data = search_tickets(service_name=service_name, status=status)

    original_count = data["count"]
    cnt = 0

    for i in data["tickets"]:
        if i["service_name"] == service_name and i["status"] == status:
            cnt += 1

    assert cnt == original_count


def test_get_ticket_details_valid_ticket(ticket_id: str = "TKT-1001"):
    data = get_ticket_details(ticket_id=ticket_id)

    found = data["found"]
    ticket = data["ticket"]

    assert found == True
    assert ticket[0]["ticket_id"] == ticket_id
    assert ticket[0]["service_name"] == "Payment API"
    assert ticket[0]["priority"]


def test_get_ticket_details_invalid_ticket(ticket_id: str = "TKT-9999"):
    data = get_ticket_details(ticket_id=ticket_id)

    found = data["found"]
    message = data["message"]

    assert found == False
    assert message


def test_high_priority_tickets_only_returns_p1_p2():
    data = get_high_priority_tickets()

    original_count = data["count"]
    tickets = data["tickets"]
    cnt = 0

    for ticket in tickets:
        if (ticket["priority"] == "P1" or ticket["priority"] == "P2") and ticket["status"] == "OPEN":
            cnt += 1

    assert cnt == original_count