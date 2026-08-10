import json
from groq_client import call_groq_model
from prompts import *
from output_parser import parse_json
# from output_builder import build_final_output
from save_output import save_output
from validators import validate_ticket_input
from output_parser import parse_json_response


def process_ticket(customer_query):

    validate_ticket_input(customer_query)

    summary = parse_json_response(
        call_groq_model(
            ticket_summarization(customer_query)
        )
    )

    classification = parse_json_response(
        call_groq_model(
            ticket_classification(customer_query)
        )
    )

    sentiment = parse_json_response(
        call_groq_model(
            sentiment_classification(customer_query)
        )
    )

    priority_risk = parse_json_response(
        call_groq_model(
            priority_risk_prompt(customer_query)
        )
    )

    sensitive_info = parse_json_response(
        call_groq_model(
            sensitive_info_detection(customer_query)
        )
    )

    routing = parse_json_response(
        call_groq_model(
            routing_prompt(customer_query)
        )
    )

    draft_response = parse_json_response(
        call_groq_model(
            draft_generator(
                ticket_input=customer_query,
                response_tone=customer_query["response_tone"],
                business_rules=customer_query.get(
                    "business_rules",
                    []
                )
            )
        )
    )

    quality_review = parse_json_response(
        call_groq_model(
            quality_review(
                draft_response["draft_response"]
            )
        )
    )

    final_output = {
        "ticket_summary": ticket_summarization,
        "classification": ticket_classification,
        "sentiment_analysis": sentiment_classification,
        "priority_and_risk": priority_risk_prompt,
        "sensitive_information_check": sensitive_info_detection,
        "routing_recommendation": routing_prompt,
        "draft_customer_response": draft_generator,
        "response_quality_review": quality_review,
        "generation_metadata": {
            "model_used": "llama-3.3-70b-versatile",
            "temperature": 0.2,
            "total_steps_completed": 8
        }
    }

    return final_output






















































