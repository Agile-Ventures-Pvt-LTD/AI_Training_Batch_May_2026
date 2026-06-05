from validators import (
    validate_ticket
)


def test_empty_subject():

    ticket = {

        "ticket_subject": "",

        "ticket_body":
        "This is a valid ticket body with more than thirty characters.",

        "response_tone":
        "Professional"
    }

    errors = validate_ticket(
        ticket
    )

    assert len(errors) > 0


def test_empty_body():

    ticket = {

        "ticket_subject":
        "Billing Issue",

        "ticket_body": "",

        "response_tone":
        "Professional"
    }

    errors = validate_ticket(
        ticket
    )

    assert len(errors) > 0


def test_short_body():

    ticket = {

        "ticket_subject":
        "Billing",

        "ticket_body":
        "Too short",

        "response_tone":
        "Professional"
    }

    errors = validate_ticket(
        ticket
    )

    assert len(errors) > 0


def test_valid_ticket():

    ticket = {

        "ticket_subject":
        "Billing Issue",

        "ticket_body":
        "I was charged twice for the same invoice and need assistance immediately.",

        "response_tone":
        "Professional"
    }

    errors = validate_ticket(
        ticket
    )

    assert len(errors) == 0