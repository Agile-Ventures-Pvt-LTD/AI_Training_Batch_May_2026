import json
import os
import re
from datetime import datetime
from typing import Any

from steps.priority_escalation import evaluate_priority
from steps.response_draft import draft_customer_response
from steps.response_quality import review_response_quality
from steps.routing_recommendation import recommend_route
from steps.sensitive_info_review import review_sensitive_information
from steps.sentiment_analyze import analyze_sentiment
from steps.ticket_classify import classify_ticket
from steps.ticket_summarize import summarize_ticket
from validators import validate_inputs


INPUT_FILE = "input.json"
STEPS_DIR = "steps"
OUTPUTS_DIR = "outputs"
FINAL_OUTPUT_FILE = os.path.join(OUTPUTS_DIR, "support_ticket_intelligence_output.json")

TEXT_REPLACEMENTS = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2248": "about",
        "\u2264": "<=",
        "\u2265": ">=",
    }
)


def log_progress(message: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def save_json(path: str, data: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(clean_text(data), file, indent=2, ensure_ascii=False)
        file.write("\n")


def clean_text(value: Any) -> Any:
    if isinstance(value, str):
        text = value.translate(TEXT_REPLACEMENTS)
        text = re.sub(r"\s*\(e\.g\.,?\s*within\s+\d+\s+hours?\)", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*\(typically\s+within\s+\d+\s+hours?\)", "", text, flags=re.IGNORECASE)
        return text
    if isinstance(value, list):
        return [clean_text(item) for item in value]
    if isinstance(value, dict):
        return {key: clean_text(item) for key, item in value.items()}
    return value


def load_input(path: str = INPUT_FILE) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def _priority_score(priority: dict[str, Any]) -> int:
    risk = str(priority.get("escalation_risk", "")).upper()
    level = str(priority.get("priority", "")).upper()
    scores = {
        "LOW": 3,
        "MEDIUM": 5,
        "HIGH": 8,
        "CRITICAL": 10,
        "P1": 10,
        "P2": 8,
        "P3": 5,
        "P4": 3,
    }
    return max(scores.get(risk, 1), scores.get(level, 1))


def _needs_human_review(
    classification: dict[str, Any],
    priority: dict[str, Any],
    privacy: dict[str, Any],
) -> bool:
    category = str(classification.get("primary_category", "")).upper()
    risk = str(priority.get("escalation_risk", "")).upper()
    risky_categories = {
        "BILLING_ISSUE",
        "CANCELLATION_OR_REFUND",
        "COMPLIANCE_OR_PRIVACY",
        "ACCOUNT_ACCESS",
    }
    return (
        category in risky_categories
        or risk in {"HIGH", "CRITICAL"}
        or bool(privacy.get("sensitive_information_detected"))
    )


def build_final_output(
    ticket: dict[str, Any],
    summary: dict[str, Any],
    classification: dict[str, Any],
    sentiment: dict[str, Any],
    priority: dict[str, Any],
    privacy: dict[str, Any],
    routing: dict[str, Any],
    draft: dict[str, Any],
    qa: dict[str, Any],
) -> dict[str, Any]:
    needs_human_review = _needs_human_review(classification, priority, privacy)
    review_reasons = [
        reason
        for reason in [
            priority.get("reasoning_summary"),
            privacy.get("evidence_summary") if privacy.get("sensitive_information_detected") else "",
            routing.get("routing_reason"),
        ]
        if reason
    ]

    return {
        "ticket_intelligence": {
            "customer_name": ticket["customer_name"],
            "customer_type": ticket["customer_type"],
            "product_area": ticket["product_area"],
            "summary": summary["short_summary"],
            "customer_problem": summary["customer_problem"],
            "business_impact": summary["business_impact"],
            "customer_requested_action": summary["customer_requested_action"],
            "category": classification["primary_category"],
            "secondary_categories": classification["secondary_categories"],
            "sentiment": sentiment["sentiment"],
            "emotion_signals": sentiment["emotion_signals"],
            "priority": priority["priority"],
            "escalation_risk": priority["escalation_risk"],
            "priority_score": _priority_score(priority),
            "risk_flags": priority["risk_triggers"],
            "sensitive_information": privacy,
            "recommended_team": routing["recommended_team"],
        },
        "recommended_actions": {
            "sla_action": priority["recommended_sla_action"],
            "routing_note": routing["internal_note"],
            "required_follow_up_information": routing["required_follow_up_information"],
            "missing_information": summary["missing_information"],
            "privacy_handling": privacy["handling_recommendations"],
        },
        "agent_response": {
            "draft_response": draft["draft_response"],
            "response_strategy": draft["response_strategy"],
            "assumptions": draft["assumptions"],
            "information_needed_before_sending": draft["information_needed_before_sending"],
        },
        "quality_assurance": {
            "review_scores": qa["scores"],
            "strengths": qa["strengths"],
            "improvement_areas": qa["improvement_areas"],
            "final_review_summary": qa["final_review_summary"],
            "business_rules_checked": ticket["business_rules"],
            "needs_human_review": needs_human_review,
            "review_reason": " | ".join(review_reasons) if needs_human_review else "No major review trigger found.",
        },
    }


def run_pipeline(user_inputs: dict[str, Any]) -> dict[str, Any]:
    log_progress("Validating ticket input")
    ticket = validate_inputs(user_inputs)
    save_json(os.path.join(STEPS_DIR, "01_validated_input.json"), ticket)

    log_progress("Summarizing ticket")
    summary = summarize_ticket(ticket)
    save_json(os.path.join(STEPS_DIR, "02_ticket_summary.json"), summary)

    log_progress("Classifying issue")
    classification = classify_ticket(ticket)
    save_json(os.path.join(STEPS_DIR, "03_ticket_classification.json"), classification)

    log_progress("Reading customer sentiment")
    sentiment = analyze_sentiment(ticket)
    save_json(os.path.join(STEPS_DIR, "04_sentiment_analysis.json"), sentiment)

    log_progress("Checking priority and escalation risk")
    priority = evaluate_priority(ticket, sentiment)
    save_json(os.path.join(STEPS_DIR, "05_priority_and_escalation.json"), priority)

    log_progress("Reviewing privacy and sensitive information")
    privacy = review_sensitive_information(ticket)
    save_json(os.path.join(STEPS_DIR, "06_sensitive_information_review.json"), privacy)

    log_progress("Choosing support queue")
    routing = recommend_route(ticket, priority)
    save_json(os.path.join(STEPS_DIR, "07_routing_recommendation.json"), routing)

    log_progress("Drafting customer reply")
    draft_payload = {
        "ticket": ticket,
        "summary": summary,
        "classification": classification,
        "sentiment": sentiment,
        "priority": priority,
        "privacy": privacy,
        "routing": routing,
    }
    draft = draft_customer_response(draft_payload)
    save_json(os.path.join(STEPS_DIR, "08_customer_response_draft.json"), draft)

    log_progress("Reviewing response quality")
    qa = review_response_quality(summary, draft)
    save_json(os.path.join(STEPS_DIR, "09_response_quality_review.json"), qa)

    log_progress("Writing final output")
    final_output = build_final_output(
        ticket,
        summary,
        classification,
        sentiment,
        priority,
        privacy,
        routing,
        draft,
        qa,
    )
    save_json(FINAL_OUTPUT_FILE, final_output)
    return final_output


if __name__ == "__main__":
    try:
        result = run_pipeline(load_input())
        print(f"Pipeline completed successfully. Output saved to {FINAL_OUTPUT_FILE}")
        print(f"Recommended team: {result['ticket_intelligence']['recommended_team']}")
        print(f"Escalation risk: {result['ticket_intelligence']['escalation_risk']}")
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} file not found.")
    except json.JSONDecodeError:
        print(f"Error: {INPUT_FILE} is malformed.")
    except (EnvironmentError, RuntimeError, ValueError, KeyError) as exc:
        print(f"Error: {exc}")
