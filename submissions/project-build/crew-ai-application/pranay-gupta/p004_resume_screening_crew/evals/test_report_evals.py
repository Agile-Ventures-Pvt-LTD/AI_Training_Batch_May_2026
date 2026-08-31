import json
import pytest
from pathlib import Path
from src.config import JD_FILE_PATH, RESUMES_DIR, get_output_report_path, HUMAN_REVIEW_NOTE
from src.output_writer import load_report
from src.tools import candidate_index_lookup_tool

def load_jd_text() -> str:
    return JD_FILE_PATH.read_text(encoding="utf-8").lower()

def load_resume_text(candidate_id: str) -> str:
    result = json.loads(candidate_index_lookup_tool.run(candidate_id))
    if not result.get("found"):
        pytest.skip(f"Resume not found for {candidate_id}")
    return (RESUMES_DIR / result["resume_file"]).read_text(encoding="utf-8").lower()

EVAL_CANDIDATES = ["CAND-001", "CAND-002", "CAND-003"]

@pytest.mark.parametrize("candidate_id", EVAL_CANDIDATES)
def test_report_relevance(candidate_id):
    try:
        report = load_report(candidate_id)
    except FileNotFoundError:
        pytest.skip(f"Report not generated for {candidate_id}")
        
    assert "ai" in report["role_title"].lower() or "engineer" in report["role_title"].lower()
    
    summary_lower = report["executive_summary"].lower()
    assert any(kw in summary_lower for kw in ["python", "ai", "llm", "rag", "api", "agent", "sql"])

@pytest.mark.parametrize("candidate_id", EVAL_CANDIDATES)
def test_groundedness_no_invented_skills(candidate_id):
    try:
        report = load_report(candidate_id)
    except FileNotFoundError:
        pytest.skip(f"Report not generated for {candidate_id}")
        
    resume_text = load_resume_text(candidate_id)
    for strength in report.get("strengths", []):
        terms = [w.lower() for w in strength.split() if len(w) > 3]
        assert any(t in resume_text for t in terms), f"Strength '{strength}' not grounded"

@pytest.mark.parametrize("candidate_id", EVAL_CANDIDATES)
def test_groundedness_no_invented_projects(candidate_id):
    try:
        report = load_report(candidate_id)
    except FileNotFoundError:
        pytest.skip(f"Report not generated for {candidate_id}")
        
    resume_text = load_resume_text(candidate_id)
    for evidence in report.get("evidence", []):
        terms = [w.lower() for w in evidence.split() if len(w) > 4 and w.isalpha()]
        assert any(t in resume_text for t in terms), f"Evidence '{evidence}' not grounded"

@pytest.mark.parametrize("candidate_id", EVAL_CANDIDATES)
def test_report_recommendation_matches_score_band(candidate_id):
    try:
        report = load_report(candidate_id)
    except FileNotFoundError:
        pytest.skip(f"Report not generated for {candidate_id}")
        
    percentage = report["percentage"]
    if percentage >= 80:
        expected = "STRONG_MATCH"
    elif percentage >= 60:
        expected = "MODERATE_MATCH"
    elif percentage >= 40:
        expected = "WEAK_MATCH"
    else:
        expected = "NEEDS_MANUAL_REVIEW"
        
    assert report["recommendation"] == expected

@pytest.mark.parametrize("candidate_id", EVAL_CANDIDATES)
def test_report_overall_score_matches_category_sum(candidate_id):
    try:
        report = load_report(candidate_id)
    except FileNotFoundError:
        pytest.skip(f"Report not generated for {candidate_id}")
        
    assert 0 <= report["overall_score"] <= 40
    expected_pct = round(report["overall_score"] / 40 * 100, 1)
    assert abs(report["percentage"] - expected_pct) < 0.5

@pytest.mark.parametrize("candidate_id", EVAL_CANDIDATES)
def test_interview_questions_meet_minimum_counts(candidate_id):
    try:
        report = load_report(candidate_id)
    except FileNotFoundError:
        pytest.skip(f"Report not generated for {candidate_id}")
        
    iq = report.get("interview_questions", {})
    assert len(iq.get("technical_questions", [])) >= 3
    assert len(iq.get("project_deep_dive_questions", [])) >= 2
    assert len(iq.get("scenario_questions", [])) >= 2
    assert len(iq.get("gap_validation_questions", [])) >= 2

@pytest.mark.parametrize("candidate_id", EVAL_CANDIDATES)
def test_interview_questions_relevant_to_jd(candidate_id):
    try:
        report = load_report(candidate_id)
    except FileNotFoundError:
        pytest.skip(f"Report not generated for {candidate_id}")
        
    jd_keywords = ["python", "sql", "api", "llm", "langchain", "rag", "vector", "testing", "git", "agent"]
    all_q = []
    iq = report.get("interview_questions", {})
    for key in ["technical_questions", "project_deep_dive_questions", "scenario_questions", "gap_validation_questions"]:
        all_q.extend(iq.get(key, []))
        
    relevant = sum(1 for q in all_q if any(kw in q.lower() for kw in jd_keywords))
    assert relevant >= 2

@pytest.mark.parametrize("candidate_id", EVAL_CANDIDATES)
def test_report_has_human_review_note(candidate_id):
    try:
        report = load_report(candidate_id)
    except FileNotFoundError:
        pytest.skip(f"Report not generated for {candidate_id}")
    assert report["human_review_note"] == HUMAN_REVIEW_NOTE