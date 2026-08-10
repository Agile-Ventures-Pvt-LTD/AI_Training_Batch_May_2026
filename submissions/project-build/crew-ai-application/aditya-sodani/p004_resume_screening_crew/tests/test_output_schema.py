from src.schemas import ScreeningReport, InterviewQuestions


def test_final_report_schema_valid():
    data = {
        "candidate_id": "CAND-001",
        "candidate_name": "Test User",
        "role_title": "AI Engineer",
        "overall_score": 30,
        "max_score": 40,
        "percentage": 75.0,
        "recommendation": "MODERATE_MATCH",
        "executive_summary": "Good candidate",
        "strengths": ["Python"],
        "gaps": ["RAG"],
        "interview_focus_areas": ["LLM"],
        "interview_questions": {
            "technical_questions": ["Q1", "Q2", "Q3"],
            "project_deep_dive_questions": ["Q1", "Q2"],
            "scenario_questions": ["Q1", "Q2"],
            "gap_validation_questions": ["Q1", "Q2"]
        },
        "evidence": ["Resume"],
        "human_review_note": "This is an AI-assisted screening report based on the provided resume and job description. A human reviewer should validate the recommendation before making any recruitment decision."
    }

    report = ScreeningReport(**data)
    assert report.candidate_id == "CAND-001"