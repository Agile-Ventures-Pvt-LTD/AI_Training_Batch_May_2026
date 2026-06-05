def validate_inputs(data):
 
    # if not data["customer_name"]:
    #     raise ValueError(
    #         "Customer Name cannot be empty"
    #     )

    # if not data["customer_type"]:
    #     raise ValueError(
    #         "Customer Type required"
    #     )
    
    if not data["ticket_subject"]:
        raise ValueError(
            "Ticket Subject cannot be empty"
        )
    
    if not data["ticket_body"]:
        raise ValueError(
            "Tickey Body cannot be empty"
        )
    
    if len(data["ticket_body"]) < 30:
        raise ValueError(
            "Ticket body is required and must contain at least 30 characters."
        )

    # if not data["sla_tier"]:
    #     raise ValueError(
    #         "Customer Tier"
    #     )
    if not data["response_tone"]:
        raise ValueError(
            " Response tone must be selected."
        )
    
    if not data["previous_interaction_history"]:
        raise ValueError(
            "If previous history is provided, it should be included in the analysis"
        )
    return True