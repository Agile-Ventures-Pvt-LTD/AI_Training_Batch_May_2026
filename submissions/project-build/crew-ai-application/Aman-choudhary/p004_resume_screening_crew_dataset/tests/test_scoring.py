from src.scoring import (calculate_score,get_recommendation_band,)
def test_score_calculator_returns_valid_band():
    scores = {
        "python_programming": 5,
        "sql_database_skills": 5,
        "api_integration": 5,
        "llm_application_development": 5,
        "agent_frameworks": 5,
        "rag_understanding": 5,
        "testing_and_quality": 5,
        "communication": 5,
    }
    result = calculate_score(scores)
    assert (result["recommendation_band"]== "STRONG_MATCH")
def test_recommendation_band_strong():
    assert (get_recommendation_band(85)== "STRONG_MATCH")
def test_recommendation_band_moderate():
    assert (get_recommendation_band(70)== "MODERATE_MATCH")
def test_recommendation_band_weak():
    assert (get_recommendation_band(50)== "WEAK_MATCH")
def test_recommendation_band_manual_review():
    assert (get_recommendation_band(20)== "NEEDS_MANUAL_REVIEW")