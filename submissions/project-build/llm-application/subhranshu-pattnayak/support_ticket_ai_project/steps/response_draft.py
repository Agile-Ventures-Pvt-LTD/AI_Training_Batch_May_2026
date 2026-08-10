from prompts import draft_generation_prompt
from steps.common import checked_llm_json, format_messages


DRAFT_KEYS = [
    "draft_response",
    "response_strategy",
    "assumptions",
    "information_needed_before_sending",
]


def draft_customer_response(analysis_payload: dict) -> dict:
    return checked_llm_json(
        format_messages(draft_generation_prompt, user_input=analysis_payload),
        DRAFT_KEYS,
        "Customer response draft",
        max_tokens=1500,
    )
