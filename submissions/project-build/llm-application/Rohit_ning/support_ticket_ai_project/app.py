import json
from pathlib import Path

from validators import validate_inputs
from groq_client import call_groq_model
from output_parser import parse_json
from prompt import (
    basic_rules,
    TICKET_SUMMARY_PROMPT,
    CLASSIFICATION_PROMPT,
    SENTIMENT_PROMPT,
    PRIORITY_RISK_PROMPT,
    SENSITIVE_PROMPT,
    ROUTING_PROMPT,
    RESPONSE_PROMPT,
    QUALITY_PROMPT,
)

sample_input = {
    "customer_name": "Amit",
    "customer_type": "Premium",
    "ticket_subject": "Charged twice and no response from support",
    "ticket_body": (
        "Hi team, I cancelled my premium subscription last month, but I was still charged again "
        "this month. I also noticed that the same invoice amount appears twice on my bank statement. "
        "I contacted support two times last week but have not received any proper response. This is "
        "extremely frustrating. If this is not resolved today, I will escalate this publicly on LinkedIn "
        "and also ask our finance team to block future payments. Please refund the incorrect charge immediately. "
        "Regards, Amit"
    ),
    "product_area": "Billing and subscription",
    "previous_interaction_history": (
        "Customer says they contacted support two times last week and did not receive a proper response."
    ),
    "sla_tier": "Premium",
    "response_tone": "Professional and empathetic",
    "business_rules": [
        "Do not promise refund before verification.",
        "Do not confirm cancellation unless verified.",
        "Ask for invoice ID or registered account email if required.",
        "Escalate premium customer billing issues to billing support.",
    ],
}

validate_inputs(sample_input)

user_input = json.dumps(sample_input, indent=2)

summary = parse_json(
    call_groq_model(
        TICKET_SUMMARY_PROMPT.format(context=user_input, basic_rules=basic_rules)
    )
)

classification = parse_json(
    call_groq_model(
        CLASSIFICATION_PROMPT.format(context=user_input, basic_rules=basic_rules)
    )
)

sentiment = parse_json(
    call_groq_model(
        SENTIMENT_PROMPT.format(context=user_input, basic_rules=basic_rules)
    )
)

priority_and_risk = parse_json(
    call_groq_model(
        PRIORITY_RISK_PROMPT.format(context=user_input, basic_rules=basic_rules)
    )
)

sensitive_information = parse_json(
    call_groq_model(
        SENSITIVE_PROMPT.format(context=user_input, basic_rules=basic_rules)
    )
)

routing = parse_json(
    call_groq_model(
        ROUTING_PROMPT.format(context=user_input, basic_rules=basic_rules)
    )
)

draft_response = parse_json(
    call_groq_model(
        RESPONSE_PROMPT.format(context=user_input, basic_rules=basic_rules)
    )
)

quality_review = parse_json(
    call_groq_model(
        QUALITY_PROMPT.format(context=user_input, basic_rules=basic_rules)
    )
)

final_output = {
    "ticket_summary": summary,
    "classification": classification,
    "sentiment_analysis": sentiment,
    "priority_and_risk": priority_and_risk,
    "sensitive_information_check": sensitive_information,
    "routing_recommendation": routing,
    "draft_customer_response": draft_response,
    "response_quality_review": quality_review,
    "generation_metadata": {
        "model_used": "llama-3.3-70b-versatile",
        "temperature": 0.2,
        "total_steps_completed": 8,
    },
}

output_dir = Path("outputs")
output_dir.mkdir(parents=True, exist_ok=True)

with open(output_dir / "sample_ticket_output.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=4, ensure_ascii=False)

print("✓ Output saved to outputs/sample_ticket_output.json")
print(json.dumps(final_output, indent=4, ensure_ascii=False))
