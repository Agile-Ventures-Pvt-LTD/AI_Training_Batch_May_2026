
def validate_ticket_input(ticket_details):

    ticket_subject = ticket_details.get("ticket_subject")

    ticket_body = ticket_details.get("ticket_body")

    response_tone = ticket_details.get("response_tone")

    if not ticket_subject:
        raise ValueError("Ticket subject is required.")

    if not ticket_body:
        raise ValueError("Ticket body is required.")

    if len(ticket_body.strip()) < 30:
        raise ValueError("Ticket body is required and must contain at least 30 characters.")

    if not response_tone:
        raise ValueError("Response tone is required.")

    return True
