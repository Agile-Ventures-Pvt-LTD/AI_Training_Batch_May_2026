import pytest
from src.tools import score_calculator_tool
import json

def test_score_calculator_strong():
    scores = {k: 5 for k in ["python_programming", "sql_database_skills", "api_integration", "llm_application_development", "agent_frameworks", "rag_understanding", "testing_and_quality", "communication"]}
    result = json.loads(score_calculator_tool.run(scores))
    assert result["recommendation_band"] == "STRONG_MATCH"

def test_score_calculator_moderate(sample_category_scores):
    result = json.loads(score_calculator_tool.run(sample_category_scores))
    assert result["recommendation_band"] == "MODERATE_MATCH"

def test_score_calculator_weak():
    scores = {k: 2 for k in ["python_programming", "sql_database_skills", "api_integration", "llm_application_development", "agent_frameworks", "rag_understanding", "testing_and_quality", "communication"]}
    result = json.loads(score_calculator_tool.run(scores))
    assert result["recommendation_band"] == "WEAK_MATCH"

def test_score_calculator_needs_review():
    scores = {k: 1 for k in ["python_programming", "sql_database_skills", "api_integration", "llm_application_development", "agent_frameworks", "rag_understanding", "testing_and_quality", "communication"]}
    result = json.loads(score_calculator_tool.run(scores))
    assert result["recommendation_band"] == "NEEDS_MANUAL_REVIEW"

def test_score_calculator_invalid_scores():
    scores = {"python_programming": 10}
    result = json.loads(score_calculator_tool.run(scores))
    assert "error" in result or result["overall_score"] == 10