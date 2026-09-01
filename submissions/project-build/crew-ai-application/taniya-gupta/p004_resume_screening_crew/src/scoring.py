def calculate_recommendation_band(percentage):
    if percentage >= 80.0:
        return "STRONG_MATCH"
    elif percentage >= 60.0:
        return "MODERATE_MATCH"
    elif percentage >= 40.0:
        return "WEAK_MATCH"
    else:
        return "NEEDS_MANUAL_REVIEW"
    
def calculate_score_metrics(category_scores):
    expected_categories = [
        "python_programming",
        "sql_database_skills",
        "api_integration",
        "llm_application_development",
        "agent_frameworks",
        "rag_understanding",
        "testing_and_quality",
        "communication"
    ]
    overall_score = 0
    for cat in expected_categories:
        val = category_scores.get(cat, 0)
        
        val = int(val)
        val = max(0, min(5, val))
        overall_score += val
        
    max_score = 40
    percentage = (overall_score / max_score) * 100
    recommendation_band = calculate_recommendation_band(percentage)
    
    return {
        "overall_score": overall_score,
        "max_score": max_score,
        "percentage": round(percentage, 2),
        "recommendation_band": recommendation_band
    }