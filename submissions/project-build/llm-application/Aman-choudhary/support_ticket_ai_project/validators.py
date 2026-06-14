def validate_ticket(ticket):

    if not ticket.get("ticket_subject"):
        raise ValueError(
            "Ticket subject is required."
        )

    if not ticket.get("ticket_body"):
        raise ValueError(
            "Ticket body is required."
        )

    if len(ticket["ticket_body"]) < 30:
        raise ValueError(
            "Ticket body must contain at least 30 characters."
        )

    if not ticket.get("response_tone"):
        raise ValueError(
            "Response tone is required."
        )

    return True