from typing import Dict
RUBRIC_CATEGORIES = ["python_programming",
    "sql_database_skills",
    "api_integration",
    "llm_application_development",
    "agent_frameworks",
    "rag_understanding",
    "testing_and_quality",
    "communication",
]
MAX_SCORE = 40
MAX_CATEGORY_SCORE = 5
MIN_CATEGORY_SCORE = 0
def get_recommendation_band(percentage: float)-> str:
    """
    Determine recommendation band.
    """
    if percentage >= 80:
        return "STRONG_MATCH"
    if percentage >= 60:
        return "MODERATE_MATCH"
    if percentage >= 40:
        return "WEAK_MATCH"
    return "NEEDS_MANUAL_REVIEW"
def validate_category_scores(category_scores: Dict[str, int])-> None:
    """
    Ensures:
    - All 8 categories exist
    - Score between 0 and 5
    """
    missing_categories = [
        category
        for category in RUBRIC_CATEGORIES
        if category not in category_scores
    ]
    if missing_categories:
        raise ValueError(f"Missing categories: {missing_categories}")
    for category, score in category_scores.items():
        if category not in RUBRIC_CATEGORIES:
            raise ValueError(f"Unknown category: {category}")
        if not isinstance(score, int):
            raise ValueError(f"{category} score must be integer.")
        if (score < MIN_CATEGORY_SCORE or score > MAX_CATEGORY_SCORE):
            raise ValueError(f"{category} score must be "f"between 0 and 5.")
def calculate_score(category_scores: Dict[str, int]) -> Dict:
    """
    Calculate final score.
    """
    validate_category_scores(category_scores)
    overall_score = sum(category_scores.values())
    percentage = round((overall_score / MAX_SCORE) * 100,2,)
    recommendation_band = (get_recommendation_band(percentage))
    return {
        "category_scores": category_scores,
        "overall_score": overall_score,
        "max_score": MAX_SCORE,
        "percentage": percentage,
        "recommendation_band": recommendation_band,
    }
def get_default_scores() -> Dict[str, int]:
    """
    Returns empty rubric template.
    """
    return {
        "python_programming": 0,
        "sql_database_skills": 0,
        "api_integration": 0,
        "llm_application_development": 0,
        "agent_frameworks": 0,
        "rag_understanding": 0,
        "testing_and_quality": 0,
        "communication": 0,
    }
if __name__ == "__main__":

    sample_scores = {
        "python_programming": 4,
        "sql_database_skills": 4,
        "api_integration": 3,
        "llm_application_development": 4,
        "agent_frameworks": 3,
        "rag_understanding": 3,
        "testing_and_quality": 4,
        "communication": 4,
    }

    result = calculate_score(sample_scores)
    print(result)