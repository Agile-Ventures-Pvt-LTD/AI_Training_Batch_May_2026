import pytest
from src.scoring import (
    load_rubric,
    load_skill_synonyms,
    get_recommendation_band,
    match_skills,
    score_candidate,
    calculate_scores_direct
)


def test_load_rubric_returns_correct_structure():
    rubric = load_rubric()
    assert "categories" in rubric
    assert "max_score" in rubric
    assert rubric["max_score"] == 40
    assert len(rubric["categories"]) == 8


def test_load_skill_synonyms_returns_mapping():
    synonyms = load_skill_synonyms()
    assert "python_programming" in synonyms
    assert "rag_understanding" in synonyms
    assert len(synonyms["python_programming"]) >= 2


def test_get_recommendation_band_strong():
    assert get_recommendation_band(85) == "STRONG_MATCH"
    assert get_recommendation_band(100) == "STRONG_MATCH"


def test_get_recommendation_band_moderate():
    assert get_recommendation_band(70) == "MODERATE_MATCH"
    assert get_recommendation_band(60) == "MODERATE_MATCH"


def test_get_recommendation_band_weak():
    assert get_recommendation_band(50) == "WEAK_MATCH"
    assert get_recommendation_band(40) == "WEAK_MATCH"


def test_get_recommendation_band_needs_review():
    assert get_recommendation_band(30) == "NEEDS_MANUAL_REVIEW"
    assert get_recommendation_band(0) == "NEEDS_MANUAL_REVIEW"


def test_match_skills_finds_matches():
    jd_skills = ["Python", "SQL", "REST API", "LangChain"]
    resume = "I know Python, SQL, and REST API very well"
    result = match_skills(jd_skills, resume)
    assert "Python" in result["matched_skills"]
    assert "SQL" in result["matched_skills"]
    assert "REST API" in result["matched_skills"]
    assert "LangChain" in result["missing_skills"]


def test_match_skills_empty_jd_skills():
    result = match_skills([], "Python SQL")
    assert result["match_percentage"] == 0.0


def test_score_candidate_returns_valid_scores():
    resume = "Python developer with SQL, API, LangChain, and RAG experience"
    result = score_candidate(resume)
    assert len(result["category_scores"]) == 8
    assert 0 <= result["overall_score"] <= 40
    assert 0 <= result["percentage"] <= 100
    assert result["recommendation_band"] in ["STRONG_MATCH", "MODERATE_MATCH", "WEAK_MATCH", "NEEDS_MANUAL_REVIEW"]


def test_calculate_scores_direct():
    scores = {"python_programming": 3, "sql_database_skills": 3, "api_integration": 3, "llm_application_development": 3, "agent_frameworks": 3, "rag_understanding": 3, "testing_and_quality": 3, "communication": 3}
    result = calculate_scores_direct(scores)
    assert result["overall_score"] == 24
    assert result["percentage"] == 60.0
    assert result["max_score"] == 40