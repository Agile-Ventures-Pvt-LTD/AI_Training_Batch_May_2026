MAX_TICKET_LENGTH = 15000


class ValidationError(Exception):
    """Custom validation exception"""
    pass


def validate_ticket_input(ticket: dict) -> dict:
    """
    Validate ticket input before sending to Groq API.
    Based strictly on FR-2 requirements.
    """

    subject = ticket.get("ticket_subject", "").strip()

    if not subject:
        raise ValidationError(
            "Ticket subject cannot be empty."
        )

    body = ticket.get("ticket_body", "").strip()

    if not body:
        raise ValidationError(
            "Ticket body cannot be empty."
        )

    if len(body) < 30:
        raise ValidationError(
            "Ticket body is required and must contain at least 30 characters."
        )

    response_tone = ticket.get("response_tone", "").strip()

    if not response_tone:
        raise ValidationError(
            "Response tone must be selected."
        )

    previous_history = ticket.get(
        "previous_interaction_history",
        ""
    ).strip()

    ticket["include_previous_history"] = bool(
        previous_history
    )

    if len(body) > MAX_TICKET_LENGTH:
        raise ValidationError(
            "Ticket body is too long. Summarize it first or reduce the input size."
        )

    return ticket