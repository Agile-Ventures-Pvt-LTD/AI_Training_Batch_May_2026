def validate_ticket(ticket: dict):

    errors = []

    subject = ticket.get("ticket_subject", "").strip()
    body = ticket.get("ticket_body", "").strip()
    tone = ticket.get("response_tone", "").strip()

    if not subject:
        errors.append(
            "Ticket subject cannot be empty."
        )

    if not body:
        errors.append(
            "Ticket body cannot be empty."
        )

    if body and len(body) < 30:
        errors.append(
            "Ticket body must contain at least 30 characters."
        )

    if not tone:
        errors.append(
            "Response tone is required."
        )

    return errors