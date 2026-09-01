import os
import json
import pytest
from src.config import OUTPUT_PATH
from src.crew import run_screening_for_candidate

@pytest.mark.integration
def test_single_candidate_run():
    candidate_id = "CAND-001"
    json_filename = f"{candidate_id}_screening_report.json"
    md_filename = f"{candidate_id}_screening_report.md"
    
    json_path = os.path.join(OUTPUT_PATH, json_filename)
    md_path = os.path.join(OUTPUT_PATH, md_filename)
            
    report = run_screening_for_candidate(candidate_id)
    
    assert report is not None
    assert isinstance(report, dict)
    assert report.get("candidate_id") == candidate_id
    assert "Rohan Mehta" in report.get("candidate_name", "")
    assert "overall_score" in report
    assert "percentage" in report
    assert "recommendation" in report
    
    assert os.path.exists(json_path), f"JSON report file was not created at {json_path}"
    assert os.path.exists(md_path), f"Markdown report file was not created at {md_path}"
    
    with open(json_path, "r", encoding="utf-8") as f:
        saved_report = json.load(f)
        
    assert saved_report.get("candidate_id") == candidate_id
    assert saved_report.get("candidate_name") == "Rohan Mehta"
    assert "interview_questions" in saved_report
    
    iq = saved_report["interview_questions"]
    assert "technical_questions" in iq
    assert "project_deep_dive_questions" in iq
    assert "scenario_questions" in iq
    assert "gap_validation_questions" in iq
    
    assert len(iq["technical_questions"]) >= 3
    assert len(iq["project_deep_dive_questions"]) >= 2
    assert len(iq["scenario_questions"]) >= 2
    assert len(iq["gap_validation_questions"]) >= 2
