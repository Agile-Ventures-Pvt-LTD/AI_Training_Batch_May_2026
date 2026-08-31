import pytest
from pydantic import ValidationError
from src.schemas import FinalScreeningReport, CategoryScores

class TestOutputSchemaCompliance:
    def test_valid_final_report_schema(self):
        valid_data = {
            "candidate_id": "CAND-001",
            "candidate_name": "Jane Doe",
            "role_title": "Senior AI Engineer",
            "overall_score": 35,
            "max_score": 40,
            "percentage": 87.5,
            "recommendation": "STRONG_MATCH",
            "executive_summary": "Exceptional candidate with extensive RAG experience.",
            "strengths": ["Python Expert", "LangChain Mastery"],
            "gaps": ["Lacks high-scale Kubernetes deployment"],
            "interview_focus_areas": ["Cloud Infrastructure"],
            "interview_questions": {
                "technical": ["Explain your indexing strategy.", "How do you mitigate prompt injection?"],
                "behavioral": ["Describe a failed agent deployment."]
            },
            "evidence": ["Worked 3 years at CoreAI Inc", "Contributed to CrewAI open source."],
            "human_review_note": "A human reviewer must validate before finalizing."
        }
        
        report = FinalScreeningReport(**valid_data)
        assert report.candidate_id == "CAND-001"
        assert report.interview_questions["technical"][0] == "Explain your indexing strategy."

    def test_schema_catches_missing_mandatory_fields(self):
        incomplete_data = {
            "candidate_id": "CAND-002",
            "candidate_name": "Rohan Kumar"

        }
        with pytest.raises(ValidationError):
            FinalScreeningReport(**incomplete_data)

    def test_category_scores_bounds_enforcement(self):
        with pytest.raises(ValidationError):
            CategoryScores(
                python_programming=6, sql_database_skills=4, api_integration=4,
                llm_application_development=4, agent_frameworks=4, rag_understanding=4,
                testing_and_quality=4, communication=4
            )
