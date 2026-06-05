import json
import os

from validators import (
    validate_ticket
)

from groq_client import (
    summarize_ticket,
    classify_ticket,
    analyze_sentiment,
    detect_priority_and_risk,
    detect_sensitive_information,
    recommend_routing,
    generate_response,
    review_response
)

from config import (
    MODEL_NAME,
    TEMPERATURE
)


def save_output(data):

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    with open(
        "outputs/sample_ticket_output.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():

    ticket = {

        "customer_name": "Amit",

        "customer_type": "Premium",

        "ticket_subject":
        "Charged twice and no response from support",

        "ticket_body":
        """
        Hi team,

        I cancelled my premium subscription
        last month but was still charged
        again this month.

        I noticed the same invoice amount
        appears twice on my bank statement.

        I contacted support two times
        last week and received no response.

        This is extremely frustrating.

        If not resolved today I will
        escalate publicly on LinkedIn.

        Please refund immediately.
        """,

        "product_area":
        "Billing and subscription",

        "response_tone":
        "Professional and empathetic"
    }

    validation_errors = (
        validate_ticket(ticket)
    )

    if validation_errors:

        print("\nValidation Errors:")

        for error in validation_errors:
            print(error)

        return

    print(
        "\nStep 1 - Ticket Summary..."
    )

    summary = summarize_ticket(
        ticket
    )

    print(
        "Step 2 - Classification..."
    )

    classification = classify_ticket(
        ticket
    )

    print(
        "Step 3 - Sentiment..."
    )

    sentiment = analyze_sentiment(
        ticket
    )

    print(
        "Step 4 - Priority..."
    )

    priority = detect_priority_and_risk(
        ticket
    )

    print(
        "Step 5 - Sensitive Information..."
    )

    sensitive = (
        detect_sensitive_information(
            ticket
        )
    )

    print(
        "Step 6 - Routing..."
    )

    routing = recommend_routing(
        ticket
    )

    print(
        "Step 7 - Response Generation..."
    )

    response = generate_response(
        ticket
    )

    print(
        "Step 8 - Response Review..."
    )

    review = review_response(
        ticket,
        response["draft_response"]
    )

    final_output = {

        "ticket_summary":
        summary,

        "classification":
        classification,

        "sentiment_analysis":
        sentiment,

        "priority_and_risk":
        priority,

        "sensitive_information_check":
        sensitive,

        "routing_recommendation":
        routing,

        "draft_customer_response":
        response,

        "response_quality_review":
        review,

        "generation_metadata": {

            "model_used":
            MODEL_NAME,

            "temperature":
            TEMPERATURE,

            "total_steps_completed":
            8
        }
    }

    save_output(
        final_output
    )

    print(
        "\nAnalysis Complete"
    )

    print(
        json.dumps(
            final_output,
            indent=4
        )
    )


if __name__ == "__main__":
    main()
    