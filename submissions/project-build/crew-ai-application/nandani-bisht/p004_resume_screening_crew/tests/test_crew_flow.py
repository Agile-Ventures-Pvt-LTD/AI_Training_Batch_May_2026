import pytest
import os
import json
from src.main import run_screening

@pytest.mark.integration
def test_single_candidate_run_creates_json_report():
    candidate_id = "CAND-001"
    run_screening(candidate_id)
    output_path = f"outputs/{candidate_id}_screening_report.json"
    assert os.path.exists(output_path)
    with open(output_path, 'r') as f:
        data = json.load(f)
    assert data["candidate_id"] == candidate_id
    assert data["max_score"] == 40