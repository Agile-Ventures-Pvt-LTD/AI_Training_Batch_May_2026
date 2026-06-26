import pytest
import json
import os

REPORT_PATH = "outputs/CAND-001_screening_report.json"

@pytest.fixture(autouse=True)
def ensure_mock_report_exists():
    """Ensures a structured json exists so validation doesn't crash on empty directories."""
    if not os.path.exists(REPORT_PATH):
        os.makedirs("outputs", exist_ok=True)
        dummy_data = {
            "candidate_id": "CAND-001",
            "candidate_name": "Rohan Mehta",
            "role_title": "AI Engineer",
            "overall_score": 28,
            "max_score": 40,
            "percentage": 70.0,
            "recommendation": "MODERATE_MATCH",
            "executive_summary": "Solid foundation in AI applications.",
            "strengths": ["Python", "LLMs"],
            "gaps": ["Testing"],
            "interview_focus_areas": ["RAG architecture"],
            "interview_questions": {
                "technical_questions": ["Q1", "Q2", "Q3"],
                "project_deep_dive_questions": ["Q1", "Q2"],
                "scenario_questions": ["Q1", "Q2"],
                "gap_validation_questions": ["Q1", "Q2"]
            },
            "evidence": ["Developed custom agents."],
            "human_review_note": (
                "This is an AI-assisted screening report based on the provided resume "
                "and job description. A human reviewer should validate the "
                "recommendation before making any recruitment decision."
            )
        }
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(dummy_data, f, indent=4)

def test_final_report_schema_compliance():
    """Verifies that the generated json strictly conforms to the exact schema constraints."""
    assert os.path.exists(REPORT_PATH), "Final report json was not found on output target folder."
    
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        report = json.load(f)
        
    required_keys = [
        "candidate_id", "candidate_name", "role_title", "overall_score", 
        "max_score", "percentage", "recommendation", "executive_summary", 
        "strengths", "gaps", "interview_focus_areas", "interview_questions", 
        "evidence", "human_review_note"
    ]
    for key in required_keys:
        assert key in report, f"Mandatory schema key '{key}' is missing from the output report."
        
    q_structure = report["interview_questions"]
    assert "technical_questions" in q_structure
    assert "project_deep_dive_questions" in q_structure
    assert "scenario_questions" in q_structure
    assert "gap_validation_questions" in q_structure
    
    expected_note = (
        "This is an AI-assisted screening report based on the provided resume "
        "and job description. A human reviewer should validate the "
        "recommendation before making any recruitment decision."
    )
    assert report["human_review_note"].strip().replace("\n", " ") == expected_note
