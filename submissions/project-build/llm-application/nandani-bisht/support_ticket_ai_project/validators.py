def validate_ticket_input(ticket: dict) -> list:
    errors = []
    subject = ticket.get('ticket_subject', '')
    body = ticket.get('ticket_body', '')
    tone = ticket.get('response_tone', '')

    if not subject or not subject.strip():
        errors.append('Ticket subject is required.')

    if not body or not body.strip():
        errors.append('Ticket body is required.')
    elif len(body.strip()) < 30:
        errors.append('Ticket body must contain at least 30 characters.')

    if not tone or not tone.strip():
        errors.append('Response tone is required.')

    if 'previous_interaction_history' in ticket and ticket.get('previous_interaction_history') is not None:
        if not str(ticket.get('previous_interaction_history')).strip():
            errors.append('Previous interaction history must contain text if provided.')

    return errors
