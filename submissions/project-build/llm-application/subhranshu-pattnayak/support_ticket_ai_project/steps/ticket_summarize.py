from prompts import summarize_prompt
from steps.common import checked_llm_json, format_prompt


SUMMARY_KEYS = [
    "short_summary",
    "customer_problem",
    "business_impact",
    "customer_requested_action",
    "important_context",
    "missing_information",
]


def summarize_ticket(ticket: dict) -> dict:
    return checked_llm_json(
        format_prompt(summarize_prompt, user_input=ticket),
        SUMMARY_KEYS,
        "Ticket summary",
        max_tokens=1000,
    )
