import json
import os

from validators import validate_inputs
from groq_client import call_groq_model
from output_parser import parse_json
from prompts import *  


ticket_input = {
    "customer_name": "Amit",
    "customer_type": "Premium",
    "ticket_subject": "Charged twice and no response from support",
     "ticket_body": """Hi team, I cancelled my premium subscription last 
month, but I was still charged again this month. I also noticed that 
the same invoice amount appears twice on my bank statement. I 
contacted support two times last week but have not received any proper 
response. This is extremely frustrating. If this is not resolved 
today, I will escalate this publicly on LinkedIn and also ask our 
finance team to block future payments. Please refund the incorrect 
charge immediately. Regards, Amit""",
     "product_area": "Billing and subscription",
     "previous_interaction_history": """Customer says they contacted 
support two times last week and did not receive a proper response.""",
"sla_tier": "Premium",
"response_tone": "Professional and empathetic",
"business_rules": [
"Do not promise refund before verification.",
"Do not confirm cancellation unless verified.",
"Ask for invoice ID or registered account email if required.",
"Escalate premium customer billing issues to billing support."
]
}

validate_inputs(ticket_input)

print("Inputs validated")


print("Generating Ticket Summary...." )

ticket_summary = parse_json(
    call_groq_model(
        ticket_summarization_prompt(ticket_input)
    )
)

print("Classifications....")

classification = parse_json(
    call_groq_model(
        ticket_classification_prompt(ticket_input)
    )
)

print("Sentimental Anlysis.....")
sentimental_analysis = parse_json(
    call_groq_model(
        sentiment_detection_prompt(ticket_input)
    )
)

print("Generating Priority and risk Detection...")

priority_and_risk = call_groq_model(
    prirority_escalation_detection_prompt(
        ticket_input
    ),
)

print("generating sensitive_information_check ")
sensitive_information_check = parse_json(
    call_groq_model(
        info_detection_prompt(ticket_input)
    )
)
print("Generating Routing Recommendations...")

routing_recommendation= parse_json(
    call_groq_model(
        internal_routing_prompt(ticket_input)
    )
)

print("Generating Draft Customer Response...")
draft_customer_response = parse_json(
    call_groq_model(
        draft_cust_resp_generation_prompt(ticket_input)
    )
)

print("Generating  Response quality review...")

response_quality = parse_json(
    call_groq_model(
        response_quality_review_prompt(ticket_input)
    )
)

# Final Output

final_output = {

    "ticket_summary": ticket_summary,

    "classification": classification,

    "sentiment_analysis": sentimental_analysis,

    "priority_and_risk": priority_and_risk,

    "sensitive_information_check": sensitive_information_check,

    "routing_recommendation": routing_recommendation,

    "draft_customer_response": draft_customer_response,

    "response_quality_review": response_quality,


    "generation_metadata": {
        "model_used": os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        ),
        "temperature": 0.3,
        "total_steps_completed": 8
    }
}


print("\nChecking JSON serializability...\n")

for key, value in final_output.items():
    try:
        json.dumps(value)
        print(f"{key}")
    except TypeError as e:
        print(f"{key}: {e}")

os.makedirs(
    "outputs",
    exist_ok=True
)

output_file = "outputs/sample_ticket_output.json"

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        final_output,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"\n Ticket Output saved successfully: {output_file}")
