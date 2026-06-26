import pytest
import json
from src.tools import (
    read_job_description_tool, candidate_index_lookup_tool, skill_matcher_tool
)

def test_read_job_description_tool_success():
    result = json.loads(read_job_description_tool.run(jd_path="job_description/jd_ai_engineer.md"))
    assert result["success"] is True
    assert "content" in result

def test_candidate_index_lookup_valid_candidate():
    result = json.loads(candidate_index_lookup_tool.run(candidate_id="CAND-001"))
    assert result["found"] is True
    assert result["candidate_name"] == "Rohan Mehta"

def test_candidate_index_lookup_invalid_candidate():
    result = json.loads(candidate_index_lookup_tool.run(candidate_id="CAND-999"))
    assert result["found"] is False

def test_skill_matcher_identifies_missing_skills():
    jd = "Python, SQL, Kubernetes"
    cand = "Python, SQL"
    result = json.loads(skill_matcher_tool.run(jd_skills=jd, candidate_skills=cand))
    assert "kubernetes" in [s.lower() for s in result["missing_skills"]]


