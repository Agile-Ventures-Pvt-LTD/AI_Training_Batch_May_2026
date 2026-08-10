from prompts import response_quality_review
from steps.common import checked_llm_json, format_messages


QA_KEYS = ["scores", "strengths", "improvement_areas", "final_review_summary"]


def review_response_quality(summary: dict, draft: dict) -> dict:
    return checked_llm_json(
        format_messages(
            response_quality_review,
            ticket_summary=summary,
            draft_customer_response=draft,
        ),
        QA_KEYS,
        "Response quality review",
        max_tokens=1200,
    )
