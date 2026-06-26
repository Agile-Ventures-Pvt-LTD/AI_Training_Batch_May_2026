import pytest
import os
from tools import read_job_description_tool, read_resume_tool, candidate_index_lookup_tool

def test_read_job_description_success(tmp_path):
    jd_file = tmp_path / "test_jd.md"
    jd_file.write_text("Role: AI Engineer", encoding="utf-8")
    
    result = read_job_description_tool.run(str(jd_file))
    assert result["success"] is True
    assert "AI Engineer" in result["content"]

def test_candidate_index_lookup_not_found():
    result = candidate_index_lookup_tool.run("INVALID-999")
    assert result["found"] is False
    assert "not found" in result["message"].lower()
