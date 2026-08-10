def validate_ticket(ticket):

    errors = []

    if not ticket.get("ticket_subject"):
        errors.append(
            "Ticket subject cannot be empty"
        )

    body = ticket.get("ticket_body", "")

    if not body:
        errors.append(
            "Ticket body cannot be empty"
        )

    if len(body) < 30:
        errors.append(
            "Ticket body must be at least 30 characters"
        )

    if not ticket.get("response_tone"):
        errors.append(
            "Response tone required"
        )

    if errors:
        raise ValueError(
            "\n".join(errors)
        )

    return True