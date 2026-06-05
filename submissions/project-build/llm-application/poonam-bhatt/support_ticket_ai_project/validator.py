def validate_ticket(ticket: dict):
    errors = []

    # Rule 1: subject required
    if not ticket.get("subject") or ticket["subject"].strip() == "":
        errors.append("Ticket subject cannot be empty.")

    # Rule 2: body required
    body = ticket.get("body", "")
    if not body or body.strip() == "":
        errors.append("Ticket body is required.")

    # Rule 3: body length >= 30
    elif len(body.strip()) < 30:
        errors.append("Ticket body must be at least 30 characters.")

    # Rule 4: response tone required
    if not ticket.get("response_tone"):
        errors.append("Response tone must be selected.")

    # Rule 5: history handling (optional but validated structurally)
    if ticket.get("previous_history"):
        if not isinstance(ticket["previous_history"], str):
            errors.append("Previous interaction history must be a text string.")

    # Rule 6: long input warning (soft rule)
    if len(body) > 3000:
        errors.append("Ticket body too long. Please summarize or shorten input.")

    return errors