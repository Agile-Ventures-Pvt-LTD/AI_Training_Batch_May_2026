def validate_ticket_input(ticket_data: dict) -> list:
    """Validates the customer support ticket based on business rules."""
    errors = []
    
    if not ticket_data.get("ticket_subject") or not ticket_data.get("ticket_subject").strip():
        errors.append("Ticket subject is required and cannot be empty.")
        
    ticket_body = ticket_data.get("ticket_body", "")
    if not ticket_body or len(ticket_body.strip()) < 30:
        errors.append("Ticket body is required and must contain at least 30 characters.")
        
    if not ticket_data.get("response_tone"):
        errors.append("Response tone must be selected.")
        
    return errors