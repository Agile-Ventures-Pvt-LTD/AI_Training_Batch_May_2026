import json
import os

from config import Config
from groq_client import GroqClient
from validators import validate_ticket
from output_parser import parse_json

from prompts import (
    SUMMARY_PROMPT,
    CLASSIFICATION_PROMPT,
    SENTIMENT_PROMPT,
    PRIORITY_PROMPT,
    SENSITIVE_PROMPT,
    ROUTING_PROMPT,
    RESPONSE_PROMPT,
    QUALITY_PROMPT
)


def run_prompt(client, prompt):

    response = client.call_model(prompt)

    return parse_json(response)


def main():

    ticket = {
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

    errors = validate_ticket(ticket)

    if errors:
        print("\nValidation Errors:")
        for err in errors:
            print("-", err)
        return

    client = GroqClient()

    summary = run_prompt(
        client,
        SUMMARY_PROMPT.format(ticket=ticket)
    )

    classification = run_prompt(
        client,
        CLASSIFICATION_PROMPT.format(ticket=ticket)
    )

    sentiment = run_prompt(
        client,
        SENTIMENT_PROMPT.format(ticket=ticket)
    )

    priority = run_prompt(
        client,
        PRIORITY_PROMPT.format(ticket=ticket)
    )

    sensitive = run_prompt(
        client,
        SENSITIVE_PROMPT.format(ticket=ticket)
    )

    routing = run_prompt(
        client,
        ROUTING_PROMPT.format(ticket=ticket)
    )

    draft_response = run_prompt(
        client,
        RESPONSE_PROMPT.format(
            ticket=ticket,
            tone=ticket["response_tone"]
        )
    )

    review = run_prompt(
        client,
        QUALITY_PROMPT.format(
            response=draft_response["draft_response"]
        )
    )

    final_output = {
        "ticket_summary": summary,
        "classification": classification,
        "sentiment_analysis": sentiment,
        "priority_and_risk": priority,
        "sensitive_information_check": sensitive,
        "routing_recommendation": routing,
        "draft_customer_response": draft_response,
        "response_quality_review": review,
        "generation_metadata": {
            "model_used": Config.GROQ_MODEL,
            "temperature": 0.2,
            "total_steps_completed": 8
        }
    }

    os.makedirs(
        Config.OUTPUT_DIR,
        exist_ok=True
    )

    output_path = os.path.join(
        Config.OUTPUT_DIR,
        "sample_ticket_output.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            final_output,
            f,
            indent=4
        )

    print(
        json.dumps(
            final_output,
            indent=4
        )
    )


if __name__ == "__main__":
    main()