import os
import json
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval, HallucinationMetric

from evaluation_prompts import INTERVIEW_GAP_ALIGNMENT_CRITERIA,RUBRIC_ADHERENCE_CRITERIA

def load_generated_report(candidate_id: str) -> dict:
    report_path = f"outputs/{candidate_id}_screening_report.json"
    if not os.path.exists(report_path):
        raise FileNotFoundError(
            f"Missing screening artifact for {candidate_id}. "
            f"Please execute: 'python src/main.py --candidate-id {candidate_id}' first."
        )
    with open(report_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_candidate_screening_hallucination():
    report = load_generated_report("CAND-001")
    
    actual_output = " ".join(report.get("strengths", [])) + " " + report.get("executive_summary", "")
    
    context = [
        "Candidate has extensive production experience building enterprise python tools and scalable frameworks.",
        "Profile shows deep working knowledge of FastAPI integrations, RAG database architectures, and prompt tuning."
    ]
    metric = HallucinationMetric(threshold=0.3)
    
    test_case = LLMTestCase(
        input="Extract strengths and match the candidate resume against the AI Engineer job requirements.",
        actual_output=actual_output,
        context=context
    )
    assert_test(test_case, [metric])


def test_interview_plan_gap_relevance():
    report = load_generated_report("CAND-001")

    gaps_found = ", ".join(report.get("gaps", []))
    
    questions_list = []
    questions_dict = report.get("interview_questions", {})
    if isinstance(questions_dict, dict):
        for cat, q_list in questions_dict.items():
            questions_list.extend(q_list)
            
    actual_questions_output = " ".join(questions_list)

    interview_relevance_metric = GEval(
        name="Interview Plan Gap Alignment",
        criteria=INTERVIEW_GAP_ALIGNMENT_CRITERIA,
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.7
    )

    test_case = LLMTestCase(
        input=f"Candidate gaps identified: {gaps_found}",
        actual_output=actual_questions_output
    )
    assert_test(test_case, [interview_relevance_metric])


def test_rubric_adherence_score():
    report = load_generated_report("CAND-001")

    actual_report_summary = (
        f"Recommendation Band: {report.get('recommendation')}\n"
        f"Percentage: {report.get('percentage')}\n"
        f"Overall Score: {report.get('overall_score')}\n"
        f"Strengths: {report.get('strengths')}\n"
        f"Gaps: {report.get('gaps')}"
    )

    rubric_adherence_metric = GEval(
        name="Rubric Rule Compliance",
        criteria=RUBRIC_ADHERENCE_CRITERIA,
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.7
    )

    test_case = LLMTestCase(
        input="Verify the screening data aligns with the grading criteria rules.",
        actual_output=actual_report_summary
    )
    assert_test(test_case, [rubric_adherence_metric])
