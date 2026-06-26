import pytest
from src.scoring import calculate_screening_metrics

def test_strong_match_score_boundary():
    """Checks if a perfect score correctly maps to STRONG_MATCH."""
    # Giving a score of 5 out of 5 for all 8 categories (Total = 40)
    perfect_scores = {
        "python_programming": 5, "sql_database_skills": 5, "api_integration": 5,
        "llm_application_development": 5, "agent_frameworks": 5, "rag_understanding": 5,
        "testing_and_quality": 5, "communication": 5
    }
    result = calculate_screening_metrics(perfect_scores)
    assert result["recommendation_band"] == "STRONG_MATCH"
    assert result["overall_score"] == 40
    assert result["percentage"] == 100

def test_needs_review_score_boundary():
    """Checks if a very low score maps to NEEDS_MANUAL_REVIEW."""
    # Giving a score of 1 out of 5 for all 8 categories (Total = 8)
    low_scores = {k: 1 for k in [
        "python_programming", "sql_database_skills", "api_integration",
        "llm_application_development", "agent_frameworks", "rag_understanding",
        "testing_and_quality", "communication"
    ]}
    result = calculate_screening_metrics(low_scores)
    assert result["recommendation_band"] == "NEEDS_MANUAL_REVIEW"
    assert result["percentage"] == 20
