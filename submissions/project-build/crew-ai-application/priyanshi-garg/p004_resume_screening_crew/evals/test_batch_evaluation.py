import pytest
import json
import os

OUTPUTS_DIR = "outputs"
TARGET_CANDIDATES = ["CAND-001", "CAND-002", "CAND-003"]

@pytest.mark.parametrize("candidate_id", TARGET_CANDIDATES)
def test_candidate_report_evaluation_criteria(candidate_id):
    """Audits each generated report file against the 5 structural evaluation criteria points."""
    file_path = os.path.join(OUTPUTS_DIR, f"{candidate_id}_screening_report.json")
    
    assert os.path.exists(file_path), f"Error: {candidate_id} ki real screening report outputs folder me nahi mili!"
    
    with open(file_path, "r", encoding="utf-8") as f:
        report = json.load(f)
        
    
    assert "role_title" in report and report["role_title"] != "", "Report lacks proper job alignment markers."
    assert len(report.get("evidence", [])) > 0, "Report does not contain textual alignment matching evidence pointers."
    
    
    assert "executive_summary" in report and len(report["executive_summary"]) > 20, "Executive summary is missing or too generic."
    assert report["candidate_id"] == candidate_id, "Metadata parameter corruption detected."
    
    
    assert "gaps" in report and isinstance(report["gaps"], list), "Gaps array missing from processing tracking logic."
    assert "interview_focus_areas" in report, "Targeted focus domains omitted."
    
    pct = report.get("percentage", 0)
    rec = report.get("recommendation", "")
    
    if pct >= 80:
        assert rec == "STRONG_MATCH"
    elif pct >= 60:
        assert rec == "MODERATE_MATCH"
    elif pct >= 40:
        assert rec == "WEAK_MATCH"
    else:
        assert rec == "NEEDS_MANUAL_REVIEW"
        
    q_dict = report.get("interview_questions", {})
    assert len(q_dict.get("technical_questions", [])) > 0, "No technical questions generated."
    assert "Q1" not in q_dict.get("technical_questions", [])[0], "Placeholder questions detected."
