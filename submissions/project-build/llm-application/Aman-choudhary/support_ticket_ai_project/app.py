import os 
from validators import validate_ticket
from groq_client import call_groq
from output_parser import parse_json
from prompts import *
import json
ticket = {
    "customer_name": "Aman",
    "customer_type": "Premium",
    "ticket_subject": "Charged twice",
    "ticket_body":
    "I cancelled my subscription but was charged twice",
    "response_tone":
    "Professional and empathetic"
}
validate_ticket(ticket)
summary = parse_json(call_groq(summarization_prompt(ticket)))
classification = parse_json(call_groq(classification_prompt(ticket)))
sentiment = parse_json(call_groq(sentiment_prompt(ticket)))
risk = parse_json(call_groq(risk_prompt(ticket)))
sensitive = parse_json(call_groq( sensitive_info_prompt(ticket)))
routing = parse_json( call_groq(routing_prompt(ticket)))
draft_response = parse_json(call_groq(response_prompt(ticket)))
review = parse_json(call_groq(quality_review_prompt(ticket)))
final_output = {
    "ticket_summary": summary,
    "classification": classification,
    "sentiment_analysis": sentiment,
    "priority_and_risk": risk,
    "sensitive_information_check": sensitive,
    "routing_recommendation": routing,
    "draft_customer_response": draft_response,
    "response_quality_review": review
}
os.makedirs("outputs", exist_ok=True)
with open(
    "outputs/sample_ticket_output.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        final_output,
        f,
        indent=4
    )
print("Analysis Complete")
