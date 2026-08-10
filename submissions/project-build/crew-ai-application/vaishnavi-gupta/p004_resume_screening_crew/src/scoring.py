SCORNG_PROMPT = """
Expected calculation:
    overall_score = sum(category_scores)
    max_score = 40
    percentage = overall_score / 40 * 100
    Recommendation bands:
    Percentage Recommendation
    80–100 STRONG_MATCH
    60–79 MODERATE_MATCH
    Percentage Recommendation
    40–59 WEAK_MATCH
    Below 40 NEEDS_MANUAL_REVIEW
"""