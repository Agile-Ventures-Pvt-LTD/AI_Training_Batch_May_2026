from validators import validate_ticket


def test_ticket_validation():

    ticket = {
        "ticket_subject": "Billing Issue",
        "ticket_body":
        "I was charged twice this month and need help.",
        "response_tone":
        "Professional"
    }

    assert validate_ticket(ticket)