import os
import json
import pytest


from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase


OUTPUT_PATH = "outputs"


def load_report(candidate_id):
    path = os.path.join(
        OUTPUT_PATH,
        f"{candidate_id}_screening_report.json"
    )

    assert os.path.exists(path), f"Missing report: {path}"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



def test_recommendation_matches_score_band():
    report = load_report("CAND-001")

    pct = report["percentage"]
    rec = report["recommendation"]

    if pct >= 80:
        assert rec == "STRONG_MATCH"
    elif pct >= 60:
        assert rec == "MODERATE_MATCH"
    elif pct >= 40:
        assert rec == "WEAK_MATCH"
    else:
        assert rec == "NEEDS_MANUAL_REVIEW"



def test_report_has_required_fields():
    report = load_report("CAND-001")

    required_fields = [
        "candidate_id",
        "candidate_name",
        "role_title",
        "overall_score",
        "percentage",
        "recommendation",
        "executive_summary",
        "strengths",
        "gaps",
        "interview_questions",
        "evidence",
        "human_review_note"
    ]

    for field in required_fields:
        assert field in report, f"Missing field: {field}"



def test_interview_questions_quality():
    report = load_report("CAND-001")
    q = report["interview_questions"]

    assert len(q["technical_questions"]) >= 3
    assert len(q["project_deep_dive_questions"]) >= 2
    assert len(q["scenario_questions"]) >= 2
    assert len(q["gap_validation_questions"]) >= 2


def test_groundedness_evidence_present():
    report = load_report("CAND-001")

    evidence = report.get("evidence", [])
    assert len(evidence) > 0

   
    assert any(
        "skill" in str(e).lower() or "resume" in str(e).lower()
        for e in evidence
    )



@pytest.mark.llm
def test_deepeval_relevance():
    """
    Uses DeepEval to check if summary is relevant to JD context
    """

    report = load_report("CAND-001")

    summary = report.get("executive_summary", "")
    assert len(summary) > 10, "Summary is empty"

    metric = AnswerRelevancyMetric()

    test_case = LLMTestCase(
        input="Evaluate candidate suitability for AI Engineer role",
        actual_output=summary
    )

    metric.measure(test_case)

    print(f"✅ DeepEval Score: {metric.score}")

    assert metric.score > 0.3



def test_multiple_reports_exist():
    for cid in ["CAND-001", "CAND-002", "CAND-003"]:
        path = os.path.join(
            OUTPUT_PATH,
            f"{cid}_screening_report.json"
        )
        assert os.path.exists(path), f"Missing report for {cid}"