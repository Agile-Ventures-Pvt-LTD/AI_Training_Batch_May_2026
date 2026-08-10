import os
import pytest

from src.main import run


OUTPUT_PATH = "outputs"


@pytest.mark.integration
def test_single_candidate_run_creates_json_report():
    candidate_id = "CAND-001"

    run(candidate_id)

    file_path = os.path.join(
        OUTPUT_PATH,
        f"{candidate_id}_screening_report.json"
    )

    assert os.path.exists(file_path)