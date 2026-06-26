import os
import pytest
import json
from src.tools import read_job_description, read_resume_tool, candidate_index_lookup_tool, load_screening_rubric_tool, score_calculator_tool

def test_read_job_description_tool_success():
    """Test that a real file is read successfully."""
    test_path = "test_jd.md"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write("AI Engineer Role")

    try:
        result = read_job_description._run(jd_path=test_path)
    except AttributeError:
        result = read_job_description(jd_path=test_path)

    assert result["success"] is True
    assert result["source_file"] == "test_jd.md"
    assert result["content"] == "AI Engineer Role"

    if os.path.exists(test_path):
        os.remove(test_path)

#=====================================================================================================================
def test_read_resume_tool_success():
    """Test that a candidate resume file is read successfully."""
    test_path = "test_resume.md"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write("Candidate Name: Rohan Mehta\nSkills: Python, GenAI")

    try:
        result = read_resume_tool(resume_path=test_path)
    except AttributeError:
        result = read_resume_tool._run(resume_path=test_path)

    assert result["success"] is True
    assert result["source_file"] == "test_resume.md"
    assert "Rohan Mehta" in result["content"]

    if os.path.exists(test_path):
        os.remove(test_path)

#======================================================================================================================

def test_candidate_index_lookup_success():
    """Test that a valid candidate ID returns correct details."""
    csv_dir = os.path.join("data", "p004_resume_screening_crew_dataset", "metadata")
    os.makedirs(csv_dir, exist_ok=True)
    csv_path = os.path.join(csv_dir, "candidate_index.csv")
    
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        f.write("candidate_id,candidate_name,resume_file\n")
        f.write("CAND-001,Rohan Mehta,candidate_001_rohan_mehta.md\n")
    try:
        result = candidate_index_lookup_tool(candidate_id="CAND-001")
    except AttributeError:
        result = candidate_index_lookup_tool._run(candidate_id="CAND-001")

    assert result["found"] is True
    assert result["candidate_name"] == "Rohan Mehta"
    assert result["resume_file"] == "candidate_001_rohan_mehta.md"

def test_candidate_index_lookup_invalid_id():
    """Test that an invalid candidate ID returns a clean false status."""
    try:
        result = candidate_index_lookup_tool(candidate_id="CAND-999")
    except AttributeError:
        result = candidate_index_lookup_tool._run(candidate_id="CAND-999")

    assert result["found"] is False
    assert result["message"] == "Candidate ID not found."

#==================================================================================================================================

def test_load_screening_rubric_tool_success():
    """Test that the screening rubric configuration is loaded correctly."""
    meta_dir = os.path.join("data", "p004_resume_screening_crew_dataset", "metadata")
    os.makedirs(meta_dir, exist_ok=True)
    path = os.path.join(meta_dir, "screening_rubric.json")
    
    rubric = {
        "categories": [
            "python_programming",
            "sql_database_skills",
            "api_integration",
            "llm_application_development",
            "agent_frameworks",
            "rag_understanding",
            "testing_and_quality",
            "communication"
        ],
        "score_range": "0 to 5",
        "max_score": 40
    }
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rubric, f)
    try:
        result = load_screening_rubric_tool()
    except AttributeError:
        result = load_screening_rubric_tool._run()

    assert "categories" in result
    assert result["score_range"] == "0 to 5"
    assert result["max_score"] == 40
    assert len(result["categories"]) == 8
    assert result["categories"][0] == "python_programming"

#===================================================================================================================================

def test_score_calculator_tool_moderate_match():
    """Test standard score calculations matching the exact user sample (70%)."""
    sample_scores = {
        "python_programming": 4,
        "sql_database_skills": 3,
        "api_integration": 4,
        "llm_application_development": 4,
        "agent_frameworks": 3,
        "rag_understanding": 3,
        "testing_and_quality": 3,
        "communication": 4
    }
    
    try:
        result = score_calculator_tool(category_scores=sample_scores)
    except AttributeError:
        result = score_calculator_tool._run(category_scores=sample_scores)
        
    assert result["overall_score"] == 28
    assert result["max_score"] == 40
    assert result["percentage"] == 70
    assert result["recommendation_band"] == "MODERATE_MATCH"

def test_score_calculator_tool_manual_review():
    """Test calculations for low scoring entries below 40% threshold."""
    low_scores = {
        "python_programming": 1,
        "sql_database_skills": 1
    }
    
    try:
        result = score_calculator_tool(category_scores=low_scores)
    except AttributeError:
        result = score_calculator_tool._run(category_scores=low_scores)
        
    assert result["overall_score"] == 2
    assert result["percentage"] == 5
    assert result["recommendation_band"] == "NEEDS_MANUAL_REVIEW"

#==========================================================================================================================









