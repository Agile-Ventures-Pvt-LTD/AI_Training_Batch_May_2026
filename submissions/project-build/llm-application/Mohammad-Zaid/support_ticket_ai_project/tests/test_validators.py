
from validators import validate_ticket_input


def test_valid_ticket():

    ticket_data = {
        "ticket_subject": "Billing issue",
        "ticket_body": "I was charged twice for my subscription and need help resolving it.",
        "response_tone": "Professional"
    }

    assert validate_ticket_input(ticket_data) is True


def test_missing_subject():

    ticket_data = {
        "ticket_subject": "",
        "ticket_body": "I was charged twice for my subscription and need help resolving it.",
        "response_tone": "Professional"
    }

    try:
        validate_ticket_input(ticket_data)
        assert False

    except ValueError:
        assert True


def test_short_ticket_body():

    ticket_data = {
        "ticket_subject": "Billing issue",
        "ticket_body": "Need refund",
        "response_tone": "Professional"
    }

    try:
        validate_ticket_input(ticket_data)
        assert False

    except ValueError:
        assert True
