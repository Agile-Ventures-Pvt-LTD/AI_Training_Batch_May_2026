from prompts import sensitive_information_detection_prompt
from steps.common import checked_llm_json, format_messages


PRIVACY_KEYS = [
    "sensitive_information_detected",
    "sensitive_categories",
    "evidence_summary",
    "handling_recommendations",
]


def review_sensitive_information(ticket: dict) -> dict:
    return checked_llm_json(
        format_messages(sensitive_information_detection_prompt, user_input=ticket),
        PRIVACY_KEYS,
        "Sensitive information review",
        max_tokens=1000,
    )
