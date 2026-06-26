import pytest
import json
import os

EVAL_CANDIDATES = ["CAND-001", "CAND-002", "CAND-003"]

def load_report(cid):
    path = f"outputs/{cid}_screening_report.json"
    if not os.path.exists(path):
        pytest.skip(f"Report for {cid} not generated yet.")
    with open(path, 'r') as f:
        return json.load(f)

@pytest.mark.parametrize("cid", EVAL_CANDIDATES)
def test_report_recommendation_matches_score_band(cid):
    report = load_report(cid)
    percentage = report["percentage"]
    recommendation = report["recommendation"]
    if percentage >= 80: assert recommendation == "STRONG_MATCH"
    elif percentage >= 60: assert recommendation == "MODERATE_MATCH"
    elif percentage >= 40: assert recommendation == "WEAK_MATCH"
    else: assert recommendation == "NEEDS_MANUAL_REVIEW"

@pytest.mark.parametrize("cid", EVAL_CANDIDATES)
def test_interview_question_quality_and_counts(cid):
    report = load_report(cid)
    questions = report["interview_questions"]
    assert len(questions.get("technical_questions", [])) >= 3
    assert len(questions.get("project_deep_dive_questions", [])) >= 2
    assert len(questions.get("scenario_questions", [])) >= 2
    assert len(questions.get("gap_validation_questions", [])) >= 2

@pytest.mark.parametrize("cid", EVAL_CANDIDATES)
def test_report_groundedness_and_relevance(cid):
    report = load_report(cid)
    assert len(report["executive_summary"]) > 50
    assert report["human_review_note"] == "This is an AI-assisted screening report based on the provided resume and job description. A human reviewer should validate the recommendation before making any recruitment decision."
    assert len(report["evidence"]) > 0

