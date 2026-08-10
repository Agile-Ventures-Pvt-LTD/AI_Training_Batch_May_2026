import pytest
from src.output_writer import validate_schema

def test_final_report_schema_valid():
    valid_report = {
        "candidate_id": "CAND-001", "candidate_name": "Rohan", "role_title": "AI Eng",
        "overall_score": 30, "max_score": 40, "percentage": 75.0, "recommendation": "MODERATE_MATCH",
        "executive_summary": "Good", "strengths": [], "gaps": [], "interview_focus_areas": [],
        "interview_questions": {}, "evidence": [], "human_review_note": "Note"
    }
    result = validate_schema(valid_report)
    assert result["schema_valid"] is True

def test_final_report_schema_invalid():
    invalid_report = {"candidate_id": "CAND-001"}
    result = validate_schema(invalid_report)
    assert result["schema_valid"] is False
    assert len(result["missing_fields"]) > 0