from pathlib import Path
from src.tools import (read_job_description_tool,read_resume_tool,candidate_index_lookup_tool,skill_matcher_tool,)
def test_read_job_description_tool_success():
    jd_file = ("data/p004_resume_screening_crew_dataset/"
               "job_description/jd_ai_engineer.md")
    result = read_job_description_tool(jd_file)
    assert result["success"] is True

def test_read_resume_tool_success():
    resume_dir = Path("data/p004_resume_screening_crew_dataset/resumes")
    resume_file = list(resume_dir.glob("*.md"))[0]
    result = read_resume_tool(str(resume_file))
    assert result["success"] is True
def test_candidate_index_lookup_valid_candidate():
    result = candidate_index_lookup_tool("CAND-001")
    assert result["found"] is True
def test_candidate_index_lookup_invalid_candidate():
    result = candidate_index_lookup_tool("INVALID-ID")
    assert result["found"] is False
def test_skill_matcher_identifies_missing_skills():
    jd_skills = ["Python","SQL","RAG"]
    candidate_skills = ["Python"]
    result = skill_matcher_tool(jd_skills,candidate_skills)
    assert "SQL" in result["missing_skills"]
    assert "RAG" in result["missing_skills"]