import pytest
import json
from src.scoring import calculate_score

@pytest.mark.parametrize("scores, expected_band", [
    ({"python_programming": 4, "sql_database_skills": 4, "api_integration": 4, "llm_application_development": 4, "agent_frameworks": 4, "rag_understanding": 4, "testing_and_quality": 4, "communication": 4}, "STRONG_MATCH"),
    ({"python_programming": 3, "sql_database_skills": 3, "api_integration": 3, "llm_application_development": 3, "agent_frameworks": 3, "rag_understanding": 3, "testing_and_quality": 3, "communication": 3}, "MODERATE_MATCH"),
    ({"python_programming": 2, "sql_database_skills": 2, "api_integration": 2, "llm_application_development": 2, "agent_frameworks": 2, "rag_understanding": 2, "testing_and_quality": 2, "communication": 2}, "WEAK_MATCH"),
    ({"python_programming": 1, "sql_database_skills": 1, "api_integration": 1, "llm_application_development": 1, "agent_frameworks": 1, "rag_understanding": 1, "testing_and_quality": 1, "communication": 1}, "NEEDS_MANUAL_REVIEW"),
])
def test_score_bands(scores, expected_band):
    result = calculate_score(scores)
    assert result["recommendation_band"] == expected_band