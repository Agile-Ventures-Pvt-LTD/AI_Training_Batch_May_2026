import json

from validator import validate_ticket
from groq_client import call_groq_model
from output_parser import extract_json

from prompts import (
    TICKET_SUMMARY_PROMPT,
    CLASSIFICATION_PROMPT,
    SENTIMENT_PROMPT,
    RISK_PROMPT,
    SENSITIVE_PROMPT,
    ROUTING_PROMPT,
    RESPONSE_PROMPT,
    REVIEW_PROMPT
)


def run_pipeline(ticket):

    validate_ticket(ticket)

    summary = extract_json(
        call_groq_model(
            TICKET_SUMMARY_PROMPT(ticket)
        )
    )

    classification = extract_json(
        call_groq_model(
            CLASSIFICATION_PROMPT(ticket)
        )
    )

    sentiment = extract_json(
        call_groq_model(
            SENTIMENT_PROMPT(ticket)
        )
    )

    risk = extract_json(
        call_groq_model(
            RISK_PROMPT(ticket)
        )
    )

    sensitive = extract_json(
        call_groq_model(
            SENSITIVE_PROMPT(ticket)
        )
    )

    routing = extract_json(
        call_groq_model(
            ROUTING_PROMPT(
                ticket,
                classification,
                risk
            )
        )
    )

    response = extract_json(
        call_groq_model(
            RESPONSE_PROMPT(ticket),
            max_tokens=1500
        )
    )

    review = extract_json(
        call_groq_model(
            REVIEW_PROMPT(response)
        )
    )

    final_output = {
        "ticket_summary": summary,
        "classification": classification,
        "sentiment_analysis": sentiment,
        "priority_and_risk": risk,
        "sensitive_information_check": sensitive,
        "routing_recommendation": routing,
        "draft_customer_response": response,
        "response_quality_review": review,
        "generation_metadata": {
            "model_used":
            "llama-3.3-70b-versatile",
            "temperature": 0.2,
            "total_steps_completed": 8
        }
    }

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

    return final_output