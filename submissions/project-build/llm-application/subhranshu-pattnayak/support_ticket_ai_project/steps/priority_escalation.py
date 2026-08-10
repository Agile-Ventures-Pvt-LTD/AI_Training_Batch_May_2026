from prompts import escalation_and_priority_prompt
from steps.common import checked_llm_json, format_messages


PRIORITY_KEYS = [
    "priority",
    "escalation_risk",
    "risk_triggers",
    "recommended_sla_action",
    "reasoning_summary",
]


def evaluate_priority(ticket: dict, sentiment: dict) -> dict:
    return checked_llm_json(
        format_messages(
            escalation_and_priority_prompt,
            user_input=ticket,
            sentiment_analysis=sentiment,
        ),
        PRIORITY_KEYS,
        "Priority and escalation analysis",
        max_tokens=1000,
    )
