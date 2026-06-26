import pytest
from scoring import score_calculator_tool
from tools import skill_matcher_tool

def test_skill_matcher_math():
    jd_skills = ["Python", "SQL", "Docker"]
    cand_skills = ["Python", "Docker"]
    
    result = skill_matcher_tool.run(jd_skills=jd_skills, candidate_skills=cand_skills)
    
    assert "Python" in result["matched_skills"]
    assert "SQL" in result["missing_skills"]
    assert result["match_percentage"] > 60

def test_score_calculator_bands():
    scores = {
        "python_programming": 4,
        "sql_database_skills": 3,
        "api_integration": 4,
        "llm_application_development": 4,
        "agent_frameworks": 3,
        "rag_understanding": 3,
        "testing_and_quality": 3,
        "communication": 4
    }
    result = score_calculator_tool.run(category_scores=scores)
    assert result["overall_score"] == 28
    assert result["recommendation_band"] == "MODERATE_MATCH"
