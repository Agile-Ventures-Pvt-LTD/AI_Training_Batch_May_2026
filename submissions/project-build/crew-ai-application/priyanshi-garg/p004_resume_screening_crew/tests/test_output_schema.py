import pytest
from tools import validate_report_schema_tool

def test_validate_schema_success():
    valid_data = {
        "candidate_id": "CAND-001",
        "candidate_name": "Rohan Mehta",
        "role_title": "AI Engineer",
        "overall_score": 28,
        "max_score": 40,
        "percentage": 70.0,
        "recommendation": "MODERATE_MATCH",
        "recommendation_band": "MODERATE_MATCH",
        "executive_summary": "Solid foundational knowledge in core architectures.",
        "strengths": ["Python Development", "LLM Fine-tuning"],
        "gaps": ["Continuous Integration testing structures"],
        "interview_focus_areas": ["Enterprise scaling applications"],
        "interview_questions": {
            "technical_questions": ["Q1", "Q2", "Q3"],
            "project_deep_dive_questions": ["Q1", "Q2"],
            "scenario_questions": ["Q1", "Q2"],
            "gap_validation_questions": ["Q1", "Q2"]
        },
        "evidence": ["Implemented custom automated workflows."],
        "category_scores": {
            "python_programming": 4,
            "sql_database_skills": 3,
            "api_integration": 4,
            "llm_application_development": 4,
            "agent_frameworks": 3,
            "rag_understanding": 3,
            "testing_and_quality": 3,
            "communication": 4
        },
        "human_review_note": (
            "This is an AI-assisted screening report based on the provided resume "
            "and job description. A human reviewer should validate the "
            "recommendation before making any recruitment decision."
        )
    }
    
    result = validate_report_schema_tool.run(report_data=valid_data)
    assert result["schema_valid"] is True

def test_validate_schema_missing_fields():
    invalid_data = {
        "candidate_id": "CAND-001"
    }
    
    result = validate_report_schema_tool.run(report_data=invalid_data)
    assert result["schema_valid"] is False
    assert len(result["missing_fields"]) > 0
