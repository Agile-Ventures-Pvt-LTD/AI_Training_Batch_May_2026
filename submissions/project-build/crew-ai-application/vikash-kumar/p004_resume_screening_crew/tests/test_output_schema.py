import pytest
from tools import read_job_description_tool,validate_report_schema_tool,skill_matcher_tool,save_report_tool,score_calculator_tool,load_screening_rubric_tool,candidate_index_lookup_tool,read_resume_tool,read_job_description_tool
from schemas import valid_lookup_output_schema,jd_schema_analyst_output_schema,resume_extraction_output_schema,skill_matching_output_schmea,interview_planning_output_schmea,final_recommendation_output_schema,gap_analysis_output_schema,agent_review_output_schmea

@pytest.mark.evaluation
def test_read_job_description_tool_success():
    jd_output = read_job_description_tool
    assert jd_output == jd_schema_analyst_output_schema

def test_read_resume_tool_success():
    read_tool = read_resume_tool
    assert read_tool == resume_extraction_output_schema

def test_candidate_index_lookup_valid_candidate():
    look_up=candidate_index_lookup_tool
    assert look_up == valid_lookup_output_schema

def test_score_calculator_returns_valid_band():
    score = score_calculator_tool
    assert score == score

def test_skill_matcher_identifies_missing_skills():
    skill = skill_matcher_tool
    assert skill == skill_matching_output_schmea

def test_final_report_schema_valid():
    final = validate_report_schema_tool
    assert final == final_recommendation_output_schema

def test_single_candidate_run_creates_json_report():
    pass