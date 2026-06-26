import json
import pytest
from src.tools import (
    read_job_description_tool, read_resume_tool, candidate_index_lookup_tool,
    load_screening_rubric_tool, score_calculator_tool, save_report_tool,
    skill_matcher_tool, validate_report_schema_tool
)

def test_read_job_description_tool_success(sample_jd_path):
    result = json.loads(read_job_description_tool.run(sample_jd_path))
    assert result["success"] is True

def test_read_resume_tool_success(sample_resume_path):
    result = json.loads(read_resume_tool.run(sample_resume_path))
    assert result["success"] is True

def test_candidate_index_lookup_valid_candidate(sample_candidate_id):
    result = json.loads(candidate_index_lookup_tool.run(sample_candidate_id))
    assert result["found"] is True

def test_candidate_index_lookup_invalid_candidate():
    result = json.loads(candidate_index_lookup_tool.run("CAND-999"))
    assert result["found"] is False

def test_load_screening_rubric_tool():
    result = json.loads(load_screening_rubric_tool.run())
    assert len(result["categories"]) == 8

def test_score_calculator_tool_valid(sample_category_scores):
    result = json.loads(score_calculator_tool.run(sample_category_scores))
    assert result["overall_score"] == 28

def test_skill_matcher_identifies_missing_skills():
    result = json.loads(skill_matcher_tool.run({"jd_skills": ["Python", "SQL"], "resume_skills": ["Python"]}))
    assert "SQL" in result["missing_skills"]

def test_save_report_tool(sample_report):
    result = json.loads(save_report_tool.run({"candidate_id": "TEST-001", "report_json_str": json.dumps(sample_report)}))
    assert result["success"] is True

def test_validate_report_schema_valid(sample_report):
    result = json.loads(validate_report_schema_tool.run(json.dumps(sample_report)))
    assert result["schema_valid"] is True