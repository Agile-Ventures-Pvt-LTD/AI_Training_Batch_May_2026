import os
from src.tools import (
    read_job_description_tool,
    read_resume_tool,
    candidate_index_lookup_tool,
)

DATASET_PATH = "data"


def test_read_job_description_tool_success():
    path = os.path.join(DATASET_PATH, "job_description", "jd_ai_engineer.md")
    result = read_job_description_tool(path)
    assert result["success"] is True
    assert "content" in result


def test_read_resume_tool_success():
    path = os.path.join(DATASET_PATH, "resumes", "candidate_001_rohan_mehta.md")
    result = read_resume_tool(path)
    assert result["success"] is True
    assert "content" in result


def test_candidate_index_lookup_valid_candidate():
    result = candidate_index_lookup_tool("CAND-001")
    assert result["found"] is True
    assert result["candidate_id"] == "CAND-001"


def test_candidate_index_lookup_invalid_candidate():
    result = candidate_index_lookup_tool("INVALID_ID")
    assert result["found"] is False
