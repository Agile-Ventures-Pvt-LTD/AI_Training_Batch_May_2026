#get user input for the blog post details
def get_user_input():
    print("Please provide the following information for ticket Generation:")
    
    customer_name = input("Customer Name: ".strip())
    customer_type = input("Customer Type (e.g., Free, paid, premium, enterprise): ".strip())
    ticket_subject = input("Ticket Subject: ".strip())
    ticket_body = input("Ticket Body: ".strip())
    product_area = input("Product Area (e.g., Billing, Technical Support, login): ".strip())
    previous_interaction_history = input("Previous Interaction History (if any): ".strip())
    sla_tier = input("SLA Tier (e.g., Standard, premium, enterprise): ".strip())
    response_tone = input("Response Tone (e.g., Professional, empathetic, concise, formal): ".strip())
    bussiness_rules = input("Business Rules (if any): ".strip())
    
customer_details = get_user_input()

def validate_customer_details(customer_details):
    ticket_subject = customer_details.get("ticket_subject")
    ticket_body = customer_details.get("ticket_body")
    response_tone = customer_details.get("response_tone")
    
    if not ticket_subject:
        raise ValueError("Ticket Subject is required.")
    if not ticket_body:
        raise ValueError("Ticket Body is required.")
    if not response_tone:
        raise ValueError("Response Tone is required.")
    return customer_details

validate_customer_details(customer_details)