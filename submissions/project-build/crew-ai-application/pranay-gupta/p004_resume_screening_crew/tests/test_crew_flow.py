import json
import pytest
from src.config import get_output_report_path
from src.output_writer import load_report

@pytest.mark.integration
def test_single_candidate_run_creates_json_report(sample_candidate_id):
    from src.crew import ResumeScreeningCrew
    crew = ResumeScreeningCrew()
    crew.run(sample_candidate_id)
    
    report_path = get_output_report_path(sample_candidate_id)
    assert report_path.exists()
    
    saved = json.loads(report_path.read_text(encoding="utf-8"))
    assert saved["candidate_id"] == sample_candidate_id

@pytest.mark.integration
def test_crew_produces_valid_recommendation(sample_candidate_id):
    from src.crew import ResumeScreeningCrew
    crew = ResumeScreeningCrew()
    crew.run(sample_candidate_id)
    
    report = load_report(sample_candidate_id)
    assert report["recommendation"] in ["STRONG_MATCH", "MODERATE_MATCH", "WEAK_MATCH", "NEEDS_MANUAL_REVIEW"]

@pytest.mark.integration
def test_sample_screening_creates_three_reports():
    from src.crew import ResumeScreeningCrew
    crew = ResumeScreeningCrew()
    crew.run_sample_screening()
    
    for cid in ["CAND-001", "CAND-002", "CAND-003"]:
        assert get_output_report_path(cid).exists()