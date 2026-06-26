from tools import score_calculator_tool
from crewai.tools import tool

@tool
def score_calculator_tool(category_scores: dict) -> dict:
    """This will evaluates the score of the candidate."""
    overall_score = sum(category_scores.values())
    max_score = 40
    
    percentage = (overall_score / max_score) * 100
    
    if percentage >= 80:
        band = "STRONG_MATCH"
    elif percentage >= 60:
        band = "MODERATE_MATCH"
    elif percentage >= 40:
        band = "WEAK_MATCH"
    else:
        band = "NEEDS_MANUAL_REVIEW"
        
    return {
        "overall_score": overall_score,
        "max_score": max_score,
        "percentage": int(percentage) if percentage.is_integer() else round(percentage, 1),
        "recommendation_band": band
    }