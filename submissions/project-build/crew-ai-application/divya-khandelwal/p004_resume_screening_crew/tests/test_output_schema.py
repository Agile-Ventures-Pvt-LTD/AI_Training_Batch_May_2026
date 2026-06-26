import pytest
from pydantic import ValidationError
from schemas import FinalReportSchema

def test_schema_accepts_valid_data():
    """Ensures Pydantic accepts a completely filled dictionary data payload."""
    good_data = {
        "candidate_id": "candidate_001",
        "candidate_name": "Rohan Mehta",
        "role_title": "AI Engineer",
        "overall_score": 35,
        "max_score": 40,
        "percentage": 87,
        "recommendation": "STRONG_MATCH",
        "executive_summary": "Great background profile.",
        "strengths": ["Python"],
        "gaps": ["None"],
        "interview_focus_areas": ["RAG"],
        "interview_questions": [{"question": "What is RAG?", "intent": "Verify knowledge"}],
        "evidence": {"python_programming": "4 years experience"},
        "human_review_note": "Solid applicant."
    }
    model = FinalReportSchema(**good_data)
    assert model.candidate_name == "Rohan Mehta"

def test_schema_rejects_missing_data():
    """Ensures Pydantic throws an error if required keys are missing."""
    bad_data = {
        "candidate_id": "candidate_001"
        # Missing all other fields required by schemas.py
    }
    with pytest.raises(ValidationError):
        FinalReportSchema(**bad_data)
