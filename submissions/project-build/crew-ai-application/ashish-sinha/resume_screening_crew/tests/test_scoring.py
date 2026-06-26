import pytest
from src.tools import score_calculator_tool, candidate_index_lookup_tool

def test_score_calculator_returns_valid_band():
    """Validates math and structural band mapping logic for compliance parsing metrics."""
    mock_high_scores = {
        "python_programming": 5, "sql_database_skills": 4, "api_integration": 5,
        "llm_application_development": 4, "agent_frameworks": 5, "rag_understanding": 4,
        "testing_and_quality": 4, "communication": 5
    } 
    
    res = score_calculator_tool.fn(category_scores=mock_high_scores)
    assert res["percentage"] == 90.0
    assert res["recommendation_band"] == "STRONG_MATCH"

def test_candidate_index_lookup_invalid_candidate():
    """Ensures tool gracefully structural returns failure instead of raising runtime crashing traps."""
    res = candidate_index_lookup_tool.fn(candidate_id="CAND-UNKNOWN-ERROR")
    assert res["found"] is False
    assert "not found" in res["message"].lower()
