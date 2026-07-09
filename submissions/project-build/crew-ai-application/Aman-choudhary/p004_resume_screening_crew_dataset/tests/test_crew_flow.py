import json
from pathlib import Path
import pytest
from src.main import (run_candidate_screening)
@pytest.mark.integration
def test_single_candidate_run_creates_json_report():
    run_candidate_screening("CAND-001")
    report_file = Path("outputs/CAND-001_screening_report.json")
    assert report_file.exists()
    with open(report_file,"r",encoding="utf-8") as file:
        report = json.load(file)
    assert isinstance(report, dict)
    assert (report["candidate_id"]== "CAND-001")