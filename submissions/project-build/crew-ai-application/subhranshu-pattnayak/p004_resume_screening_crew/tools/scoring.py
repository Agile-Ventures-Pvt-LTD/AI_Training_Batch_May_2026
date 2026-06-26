from typing import Any
from crewai.tools import tool

@tool("Score Calculator")
def calculate_score(category_scores: dict[str, int], max_score: int) -> dict[str, Any]:
    """
    Calculates overall score, percentage and recommendation band.

    Args:
        category_scores (dict[str, int]): Dictionary containing scores for all categories.
        max_score (int): Maximum score.

    Returns:
        dict[str, Any]: Score summary.
    """

    try:
        overall_score = sum(category_scores.values())
        percentage = round((overall_score / max_score) * 100, 2)
        recommendation = ModuleNotFoundError
        if percentage >= 80:
            recommendation = "STRONG_MATCH"
        elif percentage >= 60:
            recommendation = "MODERATE_MATCH"
        elif percentage >= 40:
            recommendation = "WEAK_MATCH"
        else:
            recommendation = "NEEDS_MANUAL_REVIEW"

        return {
            "overall_score": overall_score,
            "max_score": max_score,
            "percentage": percentage,
            "recommendation_band": recommendation
        }

    except Exception as e:
        return {
            "message": str(e)
        }