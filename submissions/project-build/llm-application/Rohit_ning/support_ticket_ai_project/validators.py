def validate_inputs(ticket: dict) -> list:
    errors = []
    subject = str(ticket.get("ticket_subject", "")).strip()
    body = str(ticket.get("ticket_body", "")).strip()
    tone = str(ticket.get("response_tone", "")).strip()

    if not subject:
        errors.append("Ticket subject is required.")
    if not body:
        errors.append("Ticket body is required.")
    elif len(body) < 30:
        errors.append("Ticket body must contain at least 30 characters.")
    elif len(body) > 5000:
        errors.append("Ticket body is too long. Please summarize or shorten it.")
    if not tone:
        errors.append("Response tone is required.")
    return errors
