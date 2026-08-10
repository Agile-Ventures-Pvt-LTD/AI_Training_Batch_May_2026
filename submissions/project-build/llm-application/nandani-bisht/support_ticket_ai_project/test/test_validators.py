import pytest
from validators import validate_ticket_input


def test_validate_ticket_input_success():
    valid_ticket = {
        'ticket_subject': 'Help with billing issue',
        'ticket_body': 'I was billed twice for my subscription and need assistance.',
        'response_tone': 'Professional',
    }
    errors = validate_ticket_input(valid_ticket)
    assert errors == []


def test_validate_ticket_input_missing_subject():
    errors = validate_ticket_input({
        'ticket_subject': '',
        'ticket_body': 'This is a valid ticket body that exceeds the minimum length requirement.',
        'response_tone': 'Professional',
    })
    assert 'Ticket subject is required.' in errors


def test_validate_ticket_input_short_body():
    errors = validate_ticket_input({
        'ticket_subject': 'Billing question',
        'ticket_body': 'Too short.',
        'response_tone': 'Professional',
    })
    assert 'Ticket body must contain at least 30 characters.' in errors


def test_validate_ticket_input_missing_tone():
    errors = validate_ticket_input({
        'ticket_subject': 'Billing question',
        'ticket_body': 'I have a billing issue that needs attention from support right away.',
        'response_tone': '',
    })
    assert 'Response tone is required.' in errors
