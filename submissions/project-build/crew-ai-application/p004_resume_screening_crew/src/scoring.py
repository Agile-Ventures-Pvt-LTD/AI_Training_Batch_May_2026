from typing import Dict, Any

def calculate_screening_metrics(category_scores: Dict[str, int]) -> Dict[str, Any]:
    """
    Computes summary metrics and maps candidate score percentages to the strict status bands.  
    Args:
        category_scores (dict): A dictionary tracking scores for all 8 categories (0 to 5 each).   
    Returns:
        dict: Compiled scoring data.
    """
    max_score = 40
    overall_score = sum(category_scores.values())
    
    percentage = int((overall_score / max_score) * 100) if max_score > 0 else 0
    
    if percentage >= 80:
        recommendation_band = "STRONG_MATCH"
    elif percentage >= 60:
        recommendation_band = "MODERATE_MATCH"
    elif percentage >= 40:
        recommendation_band = "WEAK_MATCH"
    else:
        recommendation_band = "NEEDS_MANUAL_REVIEW"
        
    return {
        "overall_score": overall_score,
        "max_score": max_score,
        "percentage": percentage,
        "recommendation_band": recommendation_band
    }
