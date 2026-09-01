def is_non_empty_text(value):
    return isinstance(value, str) and value.strip() != ""

def validate_ticket_input(ticket):
    errors= []

    subject = ticket.get("ticket_subject")
    body = ticket.get("ticket_body") 
    response_tone = ticket.get("response_tone")

    if not is_non_empty_text(subject):
        errors.append("Ticket subject is required.")

    if not is_non_empty_text(body):
        errors.append("Ticket body is required.")
    elif len(body.strip()) < 30:
        errors.append("Ticket body must contain at least 30 characters." )

    if not is_non_empty_text(response_tone):
        errors.append("Response tone is required.")

    return errors

def require_valid_ticket(ticket):
    errors = validate_ticket_input(ticket)
    if errors:
        raise ValueError(" ".join(errors))
