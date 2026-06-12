from prompts import routing_recommendation_prompt
from steps.common import checked_llm_json, format_messages


ROUTING_KEYS = [
    "recommended_team",
    "routing_reason",
    "internal_note",
    "required_follow_up_information",
]


def recommend_route(ticket: dict, priority: dict) -> dict:
    return checked_llm_json(
        format_messages(
            routing_recommendation_prompt,
            user_input=ticket,
            priority_and_risk=priority,
        ),
        ROUTING_KEYS,
        "Routing recommendation",
        max_tokens=1000,
    )
