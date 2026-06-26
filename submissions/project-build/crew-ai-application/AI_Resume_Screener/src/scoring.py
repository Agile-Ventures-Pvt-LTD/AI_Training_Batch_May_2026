import os

MAX_SCORE = 40

SCORE_CATEGORIES = [
    "python_programming",
    "sql_database_skills",
    "api_integration",
    "llm_application_development",
    "agent_frameworks",
    "rag_understanding",
    "testing_and_quality",
    "communication",
]

RECOMMENDATION_BANDS = {
    "STRONG_MATCH": 80,
    "MODERATE_MATCH": 60,
    "WEAK_MATCH": 40,
    "NEEDS_MANUAL_REVIEW": 0,
}


def get_recommendation_band(percentage: float) -> str:
    if percentage >= 80:
        return "STRONG_MATCH"
    elif percentage >= 60:
        return "MODERATE_MATCH"
    elif percentage >= 40:
        return "WEAK_MATCH"
    else:
        return "NEEDS_MANUAL_REVIEW"


def calculate_score(category_scores: dict) -> dict:
    overall_score = sum(category_scores.get(c, 0) for c in SCORE_CATEGORIES)
    percentage = round(overall_score / MAX_SCORE * 100, 2)
    return {
        "category_scores": category_scores,
        "overall_score": overall_score,
        "max_score": MAX_SCORE,
        "percentage": percentage,
        "recommendation_band": get_recommendation_band(percentage),
    }