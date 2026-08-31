def validate_inputs(data):

    if not data["customer_name"]:
        raise ValueError(
            "Customer name cannot be empty"
        )

    if not data["customer_type"]:
        raise ValueError(
            "Customer type required"
        )

    if not data["ticket_subject"]:
        raise ValueError(
            "Ticket subject required"
        )

    if len(data["ticket_body"]) < 30:
        raise ValueError(
            "Ticket body must be at least 30 characters long"
        )

    if len(data["response_tone"]) <= 0:
        raise ValueError(
            "Response tone required"
        )

    return True