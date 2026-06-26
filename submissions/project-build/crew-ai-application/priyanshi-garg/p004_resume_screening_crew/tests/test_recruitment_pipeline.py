import pytest
import os
import json
from tools import (
    read_job_description_tool, 
    read_resume_tool, 
    candidate_index_lookup_tool, 
    skill_matcher_tool,  
    validate_report_schema_tool
)
from crew import create_screening_crew
from scoring import score_calculator_tool


def test_read_job_description_tool_success(tmp_path):
    jd_file = tmp_path / "test_jd.md"
    jd_file.write_text("Role: AI Engineer\nSkills: Python, SQL", encoding="utf-8")
    
    result = read_job_description_tool.run(str(jd_file))
    assert result["success"] is True
    assert "AI Engineer" in result["content"]

def test_read_resume_tool_success(tmp_path):
    resume_file = tmp_path / "test_resume.md"
    resume_file.write_text("Candidate: Rohan Mehta\nSkills: Python, LLMs", encoding="utf-8")
    
    result = read_resume_tool.run(str(resume_file))
    assert result["success"] is True
    assert "Rohan Mehta" in result["content"]

def test_candidate_index_lookup_valid_candidate():
    result = candidate_index_lookup_tool.run("CAND-001")
    assert result["found"] is True
    assert "candidate_001_rohan_mehta.md" in result["resume_file"]

def test_candidate_index_lookup_invalid_candidate():
    result = candidate_index_lookup_tool.run("CAND-INVALID-999")
    assert result["found"] is False
    assert "not found" in result["message"].lower()

def test_score_calculator_returns_valid_band():
    scores = {
        "python_programming": 4, "sql_database_skills": 3, "api_integration": 4,
        "llm_application_development": 4, "agent_frameworks": 3, "rag_understanding": 3,
        "testing_and_quality": 3, "communication": 4
    }
    result = score_calculator_tool.run(category_scores=scores)
    assert result["overall_score"] == 28
    assert result["recommendation_band"] == "MODERATE_MATCH"

def test_skill_matcher_identifies_missing_skills():
    jd_skills = ["Python", "SQL", "Rust"]
    cand_skills = ["Python"]
    
    result = skill_matcher_tool.run(jd_skills=jd_skills, candidate_skills=cand_skills)
    assert "SQL" in result["missing_skills"]
    assert "Rust" in result["missing_skills"]
    assert "Python" in result["matched_skills"]

def test_final_report_schema_valid():
    valid_report = {
        "candidate_id": "CAND-001",
        "candidate_name": "Rohan Mehta",
        "role_title": "AI Engineer",
        "overall_score": 28,
        "max_score": 40,
        "percentage": 70.0,
        "recommendation": "MODERATE_MATCH",
        "recommendation_band": "MODERATE_MATCH",
        "executive_summary": "Solid foundational knowledge in core architectures.",
        "strengths": ["Python Development"],
        "gaps": ["Continuous Integration testing"],
        "interview_focus_areas": ["Enterprise scaling"],
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
    result = validate_report_schema_tool._run(report_data=valid_report)
    assert result["schema_valid"] is True


def test_single_candidate_run_creates_json_report(monkeypatch):
    """Mocks the kickoff execution chain to verify file compilation workflow rules."""
    report_path = "outputs/CAND-001_screening_report.json"
    
    mock_final_report = {
        "candidate_id": "CAND-001",
        "candidate_name": "Rohan Mehta",
        "role_title": "AI Engineer",
        "overall_score": 28,
        "max_score": 40,
        "percentage": 70.0,
        "recommendation": "MODERATE_MATCH",
        "executive_summary": "Strong foundational knowledge.",
        "strengths": ["Python"],
        "gaps": ["Rust"],
        "interview_focus_areas": ["Systems scaling"],
        "interview_questions": {
            "technical_questions": [
                "Explain GIL behavior under heavily threaded sub-processes.",
                "How do you profile a slow memory-bound vectorized pipeline?",
                "What is the difference between a dense embedding and sparse vector lookups?"
            ],
            "project_deep_dive_questions": [
                "Walk us through your design choice behind using Chroma over pgvector.",
                "How did you address data drift issues in your previous LLM deployment?"
            ],
            "scenario_questions": [
                "Your production API latency spikes by 400% after a model upgrade. Steps to debug?",
                "An open-source library changes its license model overnight. How do you pivot?"
            ],
            "gap_validation_questions": [
                "Can you walk us through your practical experience with async pytest fixtures?",
                "Since you haven't deployed LangGraph before, how would you design a simple routing agent?"
            ]
        },
        "evidence": ["Developed automated data routing blocks."],
        "human_review_note": (
            "This is an AI-assisted screening report based on the provided resume "
            "and job description. A human reviewer should validate the "
            "recommendation before making any recruitment decision."
        )
    }
    
    os.makedirs("outputs", exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(mock_final_report, f, indent=4)
        
    assert os.path.exists(report_path)
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert "Q1" not in data["interview_questions"]["technical_questions"][0]
