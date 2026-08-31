import pytest
from src.schemas import ScreeningReport, InterviewQuestions, MatchScore, JDAnalysis, ResumeProfile
from src.config import HUMAN_REVIEW_NOTE

def test_final_report_schema_valid(sample_report):
    report = ScreeningReport(**sample_report)
    assert report.candidate_id == "CAND-001"
    assert report.human_review_note == HUMAN_REVIEW_NOTE

def test_final_report_missing_candidate_id(sample_report):
    incomplete = sample_report.copy()
    del incomplete["candidate_id"]
    with pytest.raises(Exception):
        ScreeningReport(**incomplete)

def test_final_report_invalid_recommendation(sample_report):
    invalid = sample_report.copy()
    invalid["recommendation"] = "EXCELLENT"
    with pytest.raises(Exception):
        ScreeningReport(**invalid)

def test_interview_questions_schema():
    iq = InterviewQuestions(
        technical_questions=["Q1", "Q2", "Q3"],
        project_deep_dive_questions=["Q1", "Q2"],
        scenario_questions=["Q1", "Q2"],
        gap_validation_questions=["Q1", "Q2"]
    )
    assert len(iq.technical_questions) >= 3

def test_match_score_schema_valid():
    ms = MatchScore(
        category_scores={k: 3 for k in ["python_programming", "sql_database_skills", "api_integration", "llm_application_development", "agent_frameworks", "rag_understanding", "testing_and_quality", "communication"]},
        overall_score=24, percentage=60.0, recommendation_band="MODERATE_MATCH"
    )
    assert ms.overall_score == 24

def test_match_score_invalid_category():
    with pytest.raises(Exception):
        MatchScore(
            category_scores={"wrong": 3}, overall_score=3, percentage=7.5, recommendation_band="NEEDS_MANUAL_REVIEW"
        )

def test_jd_analysis_schema():
    jd = JDAnalysis(role_title="AI Engineer", required_skills=["Python"])
    assert jd.role_title == "AI Engineer"

def test_resume_profile_schema():
    rp = ResumeProfile(candidate_id="CAND-001", candidate_name="Test")
    assert rp.candidate_id == "CAND-001"