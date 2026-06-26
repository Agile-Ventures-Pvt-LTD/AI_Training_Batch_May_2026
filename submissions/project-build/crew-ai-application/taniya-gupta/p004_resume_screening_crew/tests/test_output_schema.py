import pytest
from pydantic import ValidationError
from src.schema import Finalreport

def test_final_report_schema_invalid_types():
    invalid_data = {
        "candidate_id": "CAND-001",
        "candidate_name": "Rohan Mehta",
        "role_title": "AI Engineer",
        "overall_score": "string",    #invalid type: int was expected type here
        "max_score": 40,
        "percentage": 75.0,
        "recommendation": "MODERATE_MATCH",
        "executive_summary": "Summary",
        "strengths": ["Strength"],
        "gaps": ["Gap"],
        "interview_focus_areas": ["Focus"],
        "interview_questions": {
            "technical_questions": ["Q1"],
            "project_deep_dive_questions": ["Q2"],
            "scenario_questions": ["Q3"],
            "gap_validation_questions": ["Q4"]
        },
        "evidence": ["Evidence"]
    }
    
    with pytest.raises(ValidationError):
        Finalreport(**invalid_data)
