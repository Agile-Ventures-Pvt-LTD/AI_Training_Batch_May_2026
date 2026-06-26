import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scoring import evaluate_candidate_scores

def test_evaluate_candidate_scores_strong_match():
    scores = {
        "python_programming": 5,
        "sql_database_skills": 5,
        "api_integration": 4,
        "llm_application_development": 4,
        "agent_frameworks": 4,
        "rag_understanding": 4,
        "testing_and_quality": 3,
        "communication": 4
    }
    res = evaluate_candidate_scores(scores)
    assert res["overall_score"] == 33
    assert res["percentage"] == 82.5
    assert res["recommendation"] == "STRONG_MATCH"

def test_evaluate_candidate_scores_moderate_match():
    scores = {
        "python_programming": 4,
        "sql_database_skills": 3,
        "api_integration": 4,
        "llm_application_development": 3,
        "agent_frameworks": 3,
        "rag_understanding": 3,
        "testing_and_quality": 3,
        "communication": 3
    }
    res = evaluate_candidate_scores(scores)
    assert res["overall_score"] == 26
    assert res["percentage"] == 65.0
    assert res["recommendation"] == "MODERATE_MATCH"

def test_evaluate_candidate_scores_weak_match():
    scores = {
        "python_programming": 3,
        "sql_database_skills": 2,
        "api_integration": 2,
        "llm_application_development": 2,
        "agent_frameworks": 2,
        "rag_understanding": 2,
        "testing_and_quality": 2,
        "communication": 2
    }
    res = evaluate_candidate_scores(scores)
    assert res["overall_score"] == 17
    assert res["percentage"] == 42.5
    assert res["recommendation"] == "WEAK_MATCH"

def test_evaluate_candidate_scores_needs_review():
    scores = {
        "python_programming": 2,
        "sql_database_skills": 2,
        "api_integration": 1,
        "llm_application_development": 1,
        "agent_frameworks": 1,
        "rag_understanding": 1,
        "testing_and_quality": 0,
        "communication": 2
    }
    res = evaluate_candidate_scores(scores)
    assert res["overall_score"] == 10
    assert res["percentage"] == 25.0
    assert res["recommendation"] == "NEEDS_MANUAL_REVIEW"