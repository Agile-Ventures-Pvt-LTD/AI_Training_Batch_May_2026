from src.config import MAX_SCORE, RUBRIC_CATEGORIES
from src.schemas import MatchScore
from typing import Dict, Tuple

def validate_category_scores(category_scores: Dict[str, int]) -> Tuple[bool, str]:
    if not isinstance(category_scores, dict):
        return False, "Must be a dict"
        
    missing = set(RUBRIC_CATEGORIES) - set(category_scores.keys())
    extra = set(category_scores.keys()) - set(RUBRIC_CATEGORIES)
    if missing:
        return False, f"Missing: {missing}"
    if extra:
        return False, f"Unknown: {extra}"
        
    for cat, score in category_scores.items():
        if not isinstance(score, (int, float)):
            return False, f"{cat} must be numeric"
        if not (0 <= score <= 5):
            return False, f"{cat} must be 0-5"
            
    return True, ""

def calculate_overall_score(category_scores: Dict[str, int]) -> int:
    return int(sum(category_scores.values()))

def calculate_percentage(overall_score: int, max_score: int = MAX_SCORE) -> float:
    if max_score == 0:
        return 0.0
    return round((overall_score / max_score) * 100, 1)

def get_recommendation_band(percentage: float) -> str:
    if percentage >= 80:
        return "STRONG_MATCH"
    elif percentage >= 60:
        return "MODERATE_MATCH"
    elif percentage >= 40:
        return "WEAK_MATCH"
    return "NEEDS_MANUAL_REVIEW"

def calculate_score(category_scores: Dict[str, int]) -> dict:
    is_valid, error = validate_category_scores(category_scores)
    if not is_valid:
        raise ValueError(error)
        
    overall = calculate_overall_score(category_scores)
    pct = calculate_percentage(overall, MAX_SCORE)
    band = get_recommendation_band(pct)
    
    return {
        "overall_score": overall,
        "max_score": MAX_SCORE,
        "percentage": pct,
        "recommendation_band": band,
    }