from src.tools import (validate_report_schema_tool)
def test_final_report_schema_valid():
    report = {
        "candidate_id": "CAND-001",
        "candidate_name": "Rohan Mehta",
        "role_title": "AI Engineer",
        "overall_score": 30,
        "max_score": 40,
        "percentage": 75.0,
        "recommendation": "MODERATE_MATCH",
        "executive_summary": "Test Summary",
        "strengths": [],
        "gaps": [],
        "interview_focus_areas": [],
        "interview_questions": {
            "technical_questions": [],
            "project_deep_dive_questions": [],
            "scenario_questions": [],
            "gap_validation_questions": []
        },
        "evidence": [],
        "human_review_note": "Review"
    }
    result = validate_report_schema_tool(report)
    assert result["schema_valid"] is True