from src.tools import score_calculator_tool


def test_score_calculator_returns_valid_band():
    scores = {
        "python_programming": 5,
        "sql_database_skills": 5,
        "api_integration": 5,
        "llm_application_development": 5,
        "agent_frameworks": 5,
        "rag_understanding": 5,
        "testing_and_quality": 5,
        "communication": 5
    }

    result = score_calculator_tool(scores)

    assert result["overall_score"] == 40
    assert result["recommendation_band"] == "STRONG_MATCH"
