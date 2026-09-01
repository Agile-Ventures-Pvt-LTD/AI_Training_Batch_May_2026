from src.scoring import calculate_recommendation_band, calculate_score_metrics
from src.tools import score_calculator_tool

def test_calculate_recommendation_band():
    assert calculate_recommendation_band(85.0) == "STRONG_MATCH"
    assert calculate_recommendation_band(80.0) == "STRONG_MATCH"
    assert calculate_recommendation_band(79.9) == "MODERATE_MATCH"
    assert calculate_recommendation_band(60.0) == "MODERATE_MATCH"
    assert calculate_recommendation_band(59.9) == "WEAK_MATCH"
    assert calculate_recommendation_band(40.0) == "WEAK_MATCH"
    assert calculate_recommendation_band(39.9) == "NEEDS_MANUAL_REVIEW"
    assert calculate_recommendation_band(0.0) == "NEEDS_MANUAL_REVIEW"

def test_calculate_score_metrics_valid():
    category_scores = {
        "python_programming": 5,
        "sql_database_skills": 4,
        "api_integration": 3,
        "llm_application_development": 5,
        "agent_frameworks": 4,
        "rag_understanding": 4,
        "testing_and_quality": 3,
        "communication": 4
    }
    # Total is 5+4+3+5+4+4+3+4 = 32,percentage is 32/40 * 100 = 80.0
    # So the recommendation band is STRONG_MATCH
    result = calculate_score_metrics(category_scores)
    assert result["overall_score"] == 32
    assert result["max_score"] == 40
    assert result["percentage"] == 80.0
    assert result["recommendation_band"] == "STRONG_MATCH"

def test_score_calculator_tool_success():
    category_scores = {
        "python_programming": 4,
        "sql_database_skills": 3,
        "api_integration": 4,
        "llm_application_development": 4,
        "agent_frameworks": 3,
        "rag_understanding": 3,
        "testing_and_quality": 3,
        "communication": 4
    }
    # Sum: 4+3+4+4+3+3+3+4 = 28, percentage: 28/40 * 100 = 70.0 so it a  MODERATE_MATCH
    result = score_calculator_tool.func(category_scores)
    assert result["overall_score"] == 28
    assert result["percentage"] == 70.0
    assert result["recommendation_band"] == "MODERATE_MATCH"
