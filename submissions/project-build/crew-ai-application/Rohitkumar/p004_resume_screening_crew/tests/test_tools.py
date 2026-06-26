import pytest
import json
import os
from src.tools import (
    read_job_description_tool,
    read_resume_tool,
    candidate_index_lookup_tool,
    load_screening_rubric_tool,
    score_calculator_tool,
    save_report_tool,
    skill_matcher_tool,
    validate_report_schema_tool
)
from src.config import OUTPUT_PATH


def test_read_job_description_tool_success():
    result = read_job_description_tool()
    assert result["success"] is True
    assert "AI Engineer" in result["content"]
    assert result["source_file"] == "jd_ai_engineer.md"


def test_read_resume_tool_success():
    result = read_resume_tool("candidate_001_rohan_mehta.md")
    assert result["success"] is True
    assert "Rohan Mehta" in result["content"]
    assert result["source_file"] == "candidate_001_rohan_mehta.md"


def test_candidate_index_lookup_valid_candidate():
    result = candidate_index_lookup_tool("CAND-001")
    assert result["found"] is True
    assert result["candidate_id"] == "CAND-001"
    assert result["candidate_name"] == "Rohan Mehta"
    assert result["resume_file"] == "candidate_001_rohan_mehta.md"


def test_candidate_index_lookup_invalid_candidate():
    result = candidate_index_lookup_tool("CAND-999")
    assert result["found"] is False
    assert "not found" in result["message"].lower()


def test_load_screening_rubric_tool():
    result = load_screening_rubric_tool()
    assert len(result["categories"]) == 8
    assert "python_programming" in result["categories"]
    assert result["max_score"] == 40
    assert result["score_range"] == "0 to 5"


def test_score_calculator_returns_valid_band():
    scores = {
        "python_programming": 5,
        "sql_database_skills": 4,
        "api_integration": 5,
        "llm_application_development": 4,
        "agent_frameworks": 4,
        "rag_understanding": 4,
        "testing_and_quality": 4,
        "communication": 4
    }
    result = score_calculator_tool(scores)
    assert result["overall_score"] == 34
    assert result["max_score"] == 40
    assert 80 <= result["percentage"] <= 100
    assert result["recommendation_band"] == "STRONG_MATCH"


def test_skill_matcher_identifies_missing_skills():
    jd_skills = ["Python", "SQL", "RAG", "Kubernetes", "Docker"]
    resume_text = "Python developer with SQL and Docker experience"
    result = skill_matcher_tool(jd_skills, resume_text)
    assert "Python" in result["matched_skills"]
    assert "SQL" in result["matched_skills"]
    assert "Docker" in result["matched_skills"]
    assert "RAG" in result["missing_skills"] or "Kubernetes" in result["missing_skills"]


