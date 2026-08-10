from prompts import classification_prompt
from steps.common import checked_llm_json, format_prompt


CLASSIFICATION_KEYS = [
    "primary_category",
    "secondary_categories",
    "category_reasoning_summary",
    "confidence_score",
]


def classify_ticket(ticket: dict) -> dict:
    return checked_llm_json(
        format_prompt(classification_prompt, user_input=ticket),
        CLASSIFICATION_KEYS,
        "Ticket classification",
        max_tokens=1000,
    )
