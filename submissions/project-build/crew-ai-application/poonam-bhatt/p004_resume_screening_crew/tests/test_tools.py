import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools import (
    read_job_description_tool,
    read_resume_tool,
    find_resume,
    calculate_score,
    skill_matcher,
    save_report_tool,
    validate_report
)

def test_read_job_description():
    res = read_job_description_tool("data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md")
    assert res["success"] is True
    assert "AI Engineer" in res["content"]

def test_read_resume():
    resumes = find_resume("CAND-001")
    assert len(resumes) > 0
    content = read_resume_tool(resumes[0])
    assert "Rohan Mehta" in content

def test_find_resume():
    resumes = find_resume("CAND-002")
    assert len(resumes) > 0
    assert any("candidate_002" in r for r in resumes)

def test_calculate_score():
    scores = {
        "python_programming": 5,
        "sql_database_skills": 4,
        "api_integration": 4,
        "llm_application_development": 3,
        "agent_frameworks": 2,
        "rag_understanding": 3,
        "testing_and_quality": 3,
        "communication": 4
    }
    res = calculate_score(scores)
    assert res["overall_score"] == 28
    assert res["percentage"] == 70.0
    assert res["recommendation"] == "MODERATE_MATCH"

def test_skill_matcher():
    job_skills = ["python", "sql", "rag", "langchain"]
    candidate_skills = ["python", "pandas", "sql", "docker"]
    res = skill_matcher(job_skills, candidate_skills)
    assert "Python" in res["matched_skills"]
    assert "Sql" in res["matched_skills"]
    assert "Rag" in res["missing_skills"]
    assert res["match_percentage"] == 50.0

def test_save_report_and_validate():
    report_content = '{"candidate_id": "CAND-001", "candidate_name": "Rohan", "role_title": "AI Engineer", "overall_score": 28, "max_score": 40, "percentage": 70.0, "recommendation": "MODERATE_MATCH", "executive_summary": "Good", "strengths": [], "gaps": [], "interview_focus_areas": [], "interview_questions": {"technical_questions": [], "project_deep_dive_questions": [], "scenario_questions": [], "gap_validation_questions": []}, "evidence": [], "human_review_note": "Review"}'
    filepath = save_report_tool(report_content, "test_temp_report")
    assert os.path.exists(filepath)
    val_res = validate_report(filepath)
    assert "valid" not in val_res or val_res["valid"] is not False
    assert val_res["candidate_id"] == "CAND-001"
    if os.path.exists(filepath):
        os.remove(filepath)