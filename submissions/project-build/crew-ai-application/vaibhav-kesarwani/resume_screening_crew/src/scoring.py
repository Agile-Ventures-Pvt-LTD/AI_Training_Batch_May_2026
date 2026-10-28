def get_recommendation_band(percentage: int) -> str:
    """Determine recommendation band based on percentage."""
    
    if 80 <= percentage <= 100:
        return "STRONG_MATCH"
    elif 60 <= percentage <= 79:
        return "MODERATE_MATCH"
    elif 40 <= percentage <= 59:
        return "WEAK_MATCH"
    else:
        return "NEEDS_MANUAL_REVIEW"