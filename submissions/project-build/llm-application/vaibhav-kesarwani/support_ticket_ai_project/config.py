from validators import get_list_input, get_non_empty_string

data = {
    "customer_name": "Amit",
    "customer_type": "Premium",
    "ticket_subject": "Charged twice and no response from support",
    "ticket_body": "Hi team, I cancelled my premium subscription last month, but I was still charged again this month. I also noticed that the same invoice amount appears twice on my bank statement. I contacted support two times last week but have not received any proper response. This is extremely frustrating. If this is not resolved today, I will escalate this publicly on LinkedIn and also ask our finance team to block future payments. Please refund the incorrect charge immediately. Regards, Amit",
    "product_area": "Billing and subscription",
    "previous_interaction_history": "Customer says they contacted support two times last week and did not receive a proper response.",
    "sla_tier": "Premium",
    "response_tone": "Professional and empathetic",
    "business_rules": [
        "Do not promise refund before verification.",
        "Do not confirm cancellation unless verified.",
        "Ask for invoice ID or registered account email if required.",
        "Escalate premium customer billing issues to billing support."
    ]
}

def user_input():
    customer_name = input("Enter your name : ").strip()
    customer_type = input("Enter the plan in which you are like: \n Free, Paid, Premium, Enterprise : ").strip()

    ticket_subject = get_non_empty_string(
        "Enter the ticket subject",
        "Please provide the subject of the ticket."
    )

    ticket_body = get_non_empty_string(
        "Enter the ticket body",
        "Please provide the body of the ticket."
    )

    print("\nProduct area like Billing, login, dashboard, API, reports, subscription\n")
    product_area = input("Enter the product area : ").strip()

    previous_history = input("Enter the previous interaction : ").split()

    print("\nThe SLA Teir can be : Standard, premium, enterprise")
    sla_teir = input("Enter the SLA Teir").split()

    response_tone = get_non_empty_string(
        "Enter the reponse tone : ",
        "Please provide the response tone."
    )

    print("\nYou can provide the multiple business rules just comma(,) seprate them.")
    business_rules = get_list_input(
        "Enter the Business Rules : ",
        "",
        required=False
    )

    user_input_data = {
        "customer_name" : customer_name,
        "customer_type" : customer_type,
        "ticket_subject" : ticket_subject,
        "ticket_body" : ticket_body,
        "product_area" : product_area,
        "previous_history" : previous_history,
        "sla_teir" : sla_teir,
        "response_tone" : response_tone,
        "business_rules" : business_rules,
    }

    return user_input_data