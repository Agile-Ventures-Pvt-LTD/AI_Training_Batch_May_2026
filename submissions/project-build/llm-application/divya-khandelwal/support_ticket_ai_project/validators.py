def validate_groq_api_key(api_key):
    if not api_key.startswith("gsk_"):
        raise ValueError("Invalid GROQ API key format. It should start with 'gsk_'.")
    if len(api_key) < 20:
        raise ValueError("Invalid GROQ API key length. It should be at least 20 characters long.")
    
def validate_ticket_request(ticket_request):
    required_fields = [
        "customer_name",
        "customer_type",
        "ticket_subject",
        "ticket_body",
        "product_area",
        "previous_interaction_history",
        "sla_tier",
        "response_tone",
        "business_rules",
    ]

    missing_fields = [field for field in required_fields if field not in ticket_request]
    if missing_fields:
        raise ValueError(f"Missing required fields in blog request: {', '.join(missing_fields)}")
    
    if not isinstance(ticket_request["business_rules"], list):
        raise ValueError("The 'business_rules' field should be a list of strings.")
    


