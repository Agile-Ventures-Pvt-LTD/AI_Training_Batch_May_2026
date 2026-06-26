import pytest
import json
from src.schemas import FinalReport, JDRequirement, ResumeProfile, MatchScore, InterviewPlan
from src.tools import validate_report_schema_tool


def test_final_report_schema_valid():
    report = {
        "candidate_id": "CAND-001",
        "candidate_name": "Rohan Mehta",
        "role_title": "AI Engineer",
        "overall_score": 30,
        "max_score": 40,
        "percentage": 75.0,
        "recommendation": "MODERATE_MATCH",
        "executive_summary": "Test summary",
        "strengths": ["Python", "SQL"],
        "gaps": ["RAG"],
        "interview_focus_areas": ["Technical"],
        "interview_questions": {
            "technical_questions": ["Q1", "Q2", "Q3"],
            "project_deep_dive_questions": ["Q4", "Q5"],
            "scenario_questions": ["Q6", "Q7"],
            "gap_validation_questions": ["Q8", "Q9"]
        },
        "evidence": ["Evidence 1"],
        "human_review_note": "This is an AI-assisted screening report"
    }
    result = validate_report_schema_tool(report)
    assert result["schema_valid"] is True


def test_final_report_schema_missing_fields():
    report = {
        "candidate_id": "CAND-001",
        "candidate_name": "Rohan Mehta"
    }
    result = validate_report_schema_tool(report)
    assert result["schema_valid"] is False
    assert len(result["missing_fields"]) > 0


def test_final_report_pydantic_model():
    report = FinalReport(
        candidate_id="CAND-001",
        candidate_name="Rohan Mehta",
        role_title="AI Engineer",
        overall_score=30,
        max_score=40,
        percentage=75.0,
        recommendation="MODERATE_MATCH",
        executive_summary="Good candidate",
        strengths=["Python"],
        gaps=["RAG"],
        interview_focus_areas=["Focus"],
        evidence=["Test"],
        human_review_note="Review required"
    )
    assert report.candidate_id == "CAND-001"
    assert report.recommendation == "MODERATE_MATCH"


def test_jd_requirement_schema():
    jd = JDRequirement(
        role_title="AI Engineer",
        required_skills=["Python", "SQL"],
        preferred_skills=["FastAPI"],
        responsibilities=["Build AI apps"],
        experience_expectation="2-5 years",
        evaluation_criteria=["Technical", "Communication"]
    )
    assert len(jd.required_skills) == 2
    assert jd.role_title == "AI Engineer"


def test_resume_profile_schema():
    profile = ResumeProfile(
        candidate_id="CAND-001",
        candidate_name="Rohan Mehta",
        current_role="AI Developer",
        years_experience="3.5",
        skills=["Python", "SQL"],
        projects=["Project A"],
        experience_summary=["Worked at X"],
        education=["BTech"],
        certifications=["Python Cert"]
    )
    assert profile.candidate_id == "CAND-001"


def test_match_score_defaults():
    match = MatchScore()
    assert match.max_score == 40
    assert match.overall_score == 0
    assert match.category_scores.python_programming == 0


def test_interview_plan_schema():
    plan = InterviewPlan(
        interview_focus_areas=["Focus A"],
        technical_questions=["Q1", "Q2", "Q3"],
        project_deep_dive_questions=["Q4", "Q5"],
        scenario_questions=["Q6", "Q7"],
        gap_validation_questions=["Q8", "Q9"]
    )
    assert len(plan.technical_questions) >= 3
    assert len(plan.project_deep_dive_questions) >= 2