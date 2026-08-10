"""
Main Ticket Intelligence Workflow

Step 1: Accept Ticket Input
Step 2: Validate Input
Step 3: Summarize Ticket
Step 4: Classification
Step 5: Sentiment Analysis
Step 6: Priority & Escalation Risk
Step 7: Sensitive Information Detection
Step 8: Routing Recommendation
Step 9: Draft Customer Response
Step 10: Review Generated Response
Step 11: Build Final Ticket Intelligence Package
Step 12: Save Output
"""

import json
import os
from urllib import response

from validators import validate_ticket_input

from groq_client import call_groq_model

from output_parser import parse_json_response

from prompts import (
    ticket_summarization_system_prompt,
    ticket_summarization_user_prompt,

    ticket_classification_system_prompt,
    ticket_classification_user_prompt,

    sensitive_information_system_prompt,
    sensitive_information_user_prompt,

    routing_recommendation_system_prompt,
    routing_recommendation_user_prompt,

    draft_response_system_prompt,
    draft_response_user_prompt,

    quality_review_system_prompt,
    quality_review_user_prompt
)

from config import GROQ_MODEL


# ==========================================================
# STEP 1 - USER INPUT
# ==========================================================

def get_ticket_input():

    print("\nPlease provide the following information for ticket generation:\n")
    customer_name = input("Customer Name: ")
    customer_type = input("Customer Type (Free/Paid/Premium/Enterprise): ")
    ticket_subject = input("Ticket Subject: ")
    ticket_body = input("Ticket Body: ")
    product_area = input("Product Area: ")
    previous_interaction_history = input("Previous Interaction History (if any): ")
    sla_tier = input("SLA Tier: ")
    response_tone = input("Response Tone: ")
    number_of_bussiness_rule = int(input("Number of Business Rules?: "))
    business_rules = []
    for i in range(number_of_bussiness_rule):
        business_rule = input(f"Business Rule {i + 1} (if any): ")
        business_rules.append(business_rule)

    return {
        "customer_name": customer_name,
        "customer_type": customer_type,
        "ticket_subject": ticket_subject,
        "ticket_body": ticket_body,
        "product_area": product_area,
        "previous_interaction_history": previous_interaction_history,
        "sla_tier": sla_tier,
        "response_tone": response_tone,
        "business_rules": business_rules
    }


# ==========================================================
# BUILD TICKET TEXT
# ==========================================================

def build_ticket_text(ticket_details):

    return f"""
Customer Name: {ticket_details['customer_name']}
Customer Type: {ticket_details['customer_type']}

Subject:
{ticket_details['ticket_subject']}

Ticket:
{ticket_details['ticket_body']}

Product Area:
{ticket_details['product_area']}

Previous Interaction History:
{ticket_details['previous_interaction_history']}

SLA Tier:
{ticket_details['sla_tier']}
"""


# ==========================================================
# STEP 3 - SUMMARIZATION
# ==========================================================

def generate_ticket_summary(ticket_input):

    response = call_groq_model(
        system_prompt=ticket_summarization_system_prompt,
        user_prompt=ticket_summarization_user_prompt.format(
            ticket_input=ticket_input
        ),
        max_tokens=500
    )
    print("\nSummary Response:")
    print(response)
    return parse_json_response(response)


# ==========================================================
# STEP 4 + 5 + 6
# Classification + Sentiment + Priority/Risk
# ==========================================================

def generate_classification_analysis(ticket_input):

    response = call_groq_model(
        system_prompt=ticket_classification_system_prompt,
        user_prompt=ticket_classification_user_prompt.format(
            ticket_input=ticket_input
        ),
        max_tokens=700
    )
    print("\nClassification, Sentiment, Priority/Risk Response:")
    print(response)
    return parse_json_response(response)


# ==========================================================
# STEP 7
# ==========================================================

def generate_sensitive_information_check(ticket_input):

    response = call_groq_model(
        system_prompt=sensitive_information_system_prompt,
        user_prompt=sensitive_information_user_prompt.format(
            ticket_input=ticket_input
        ),
        max_tokens=400
    )
    print("\nSensitive Information Check Response:")
    print(response)

    return parse_json_response(response)


# ==========================================================
# STEP 8
# ==========================================================

def generate_routing_recommendation(ticket_input):

    response = call_groq_model(
        system_prompt=routing_recommendation_system_prompt,
        user_prompt=routing_recommendation_user_prompt.format(
            ticket_input=ticket_input
        ),
        max_tokens=400
    )
    print("\nRouting Recommendation Response:")
    print(response)
    return parse_json_response(response)


# ==========================================================
# STEP 9
# ==========================================================

def generate_draft_response(ticket_input):

    response = call_groq_model(
        system_prompt=draft_response_system_prompt,
        user_prompt=draft_response_user_prompt.format(
            ticket_input=ticket_input
        ),
        max_tokens=700
    )
    print("\nDraft Response:")
    print(response)
    return parse_json_response(response)


# ==========================================================
# STEP 10
# ==========================================================

def generate_quality_review(draft_response):

    response = call_groq_model(
        system_prompt=quality_review_system_prompt,
        user_prompt=quality_review_user_prompt.format(
            draft_response=draft_response
        ),
        max_tokens=500
    )
    print("\nQuality Review Response:")
    print(response)
    return parse_json_response(response)


# ==========================================================
# STEP 12
# ==========================================================

def save_output(final_output):

    os.makedirs("outputs", exist_ok=True)

    output_path = ("outputs/sample_ticket_output.json")

    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(final_output, f, indent=4, ensure_ascii=False)

    return output_path


# ==========================================================
# MAIN
# ==========================================================

def main():

    try:

        # Step 1
        ticket_details = get_ticket_input()

        # Step 2
        validate_ticket_input(ticket_details)
        ticket_input = build_ticket_text(ticket_details)
        print("\nGenerating ticket package...\n")

        # Step 3
        ticket_summary = generate_ticket_summary(ticket_input)

        # Step 4 + 5 + 6
        analysis_result = (generate_classification_analysis(ticket_input))

        # Step 7
        sensitive_information = (generate_sensitive_information_check(ticket_input))

        # Step 8
        routing_recommendation = (generate_routing_recommendation(ticket_input))

        # Step 9
        draft_response = (generate_draft_response(ticket_input))

        # Step 10
        quality_review = (generate_quality_review(draft_response))

        # Step 11
        final_output = {

            "ticket_summary": ticket_summary,

            "classification": analysis_result.get("classification", {}),

            "sentiment_analysis": analysis_result.get("sentiment_analysis", {}),

            "priority_and_risk": analysis_result.get("priority_and_risk", {}),

            "sensitive_information_check":sensitive_information.get("sensitive_information_check", {}),

            "routing_recommendation":routing_recommendation.get("routing_recommendation", {}),

            "draft_customer_response":
                draft_response.get("draft_customer_response", {}),

            "response_quality_review": quality_review.get("response_quality_review",{}),

            "generation_metadata": {"model_used": GROQ_MODEL
            }
        }

        output_path = save_output(final_output)

        print("\nTicket Intelligence Package Generated Successfully.")

        print(f"\nSaved to: {output_path}")

    except Exception as e:

        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()