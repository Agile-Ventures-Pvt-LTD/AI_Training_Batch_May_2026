import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import JD_FILE_PATH, RESUMES_DIR, OUTPUT_PATH

@pytest.fixture
def sample_candidate_id():
    return "CAND-001"

@pytest.fixture
def sample_resume_path():
    return str(RESUMES_DIR / "candidate_001_rohan_mehta.md")

@pytest.fixture
def sample_jd_path():
    return str(JD_FILE_PATH)

@pytest.fixture
def sample_category_scores():
    return {
        "python_programming": 4,
        "sql_database_skills": 3,
        "api_integration": 4,
        "llm_application_development": 4,
        "agent_frameworks": 3,
        "rag_understanding": 3,
        "testing_and_quality": 3,
        "communication": 4,
    }

@pytest.fixture
def sample_report():
    from src.config import HUMAN_REVIEW_NOTE
    return {
        "candidate_id": "CAND-001",
        "candidate_name": "Rohan Mehta",
        "role_title": "AI Engineer",
        "overall_score": 28,
        "max_score": 40,
        "percentage": 70.0,
        "recommendation": "MODERATE_MATCH",
        "executive_summary": "Candidate shows strong Python and API skills.",
        "strengths": ["Python programming", "REST API integration"],
        "gaps": ["Limited RAG experience"],
        "interview_focus_areas": ["RAG fundamentals", "Vector databases"],
        "interview_questions": {
            "technical_questions": ["Q1?", "Q2?", "Q3?"],
            "project_deep_dive_questions": ["Q1?", "Q2?"],
            "scenario_questions": ["Q1?", "Q2?"],
            "gap_validation_questions": ["Q1?", "Q2?"],
        },
        "evidence": ["Built 3 Python-based ML projects"],
        "human_review_note": HUMAN_REVIEW_NOTE,
    }

@pytest.fixture(autouse=True)
def ensure_output_dir():
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)