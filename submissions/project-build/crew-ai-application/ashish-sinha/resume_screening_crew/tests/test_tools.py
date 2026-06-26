import os
import json
import pytest
import pandas as pd
from src.tools import (
    read_job_description_tool, 
    read_resume_tool, 
    candidate_index_lookup_tool, 
    save_report_tool
)

class TestToolsFunctionality:
    @pytest.fixture
    def setup_mock_dataset(self, tmp_path):
        """Sets up a temporary filesystem mock layout for high-fidelity tool integration tests."""
       
        jd_dir = tmp_path / "job_description"
        resumes_dir = tmp_path / "resumes"
        metadata_dir = tmp_path / "metadata"
        outputs_dir = tmp_path / "outputs"
        
        jd_dir.mkdir()
        resumes_dir.mkdir()
        metadata_dir.mkdir()
        outputs_dir.mkdir()

        jd_file = jd_dir / "jd_ai_engineer.md"
        jd_file.write_text("# AI Engineer Job Criteria", encoding="utf-8")

        resume_file = resumes_dir / "resume_mock_01.md"
        resume_file.write_text("# Candidate Resume Data", encoding="utf-8")

        csv_file = metadata_dir / "candidate_index.csv"
        df = pd.DataFrame([{
            "candidate_id": "CAND-TEST-01",
            "candidate_name": "Alice Tester",
            "resume_file": "resume_mock_01.md"
        }])
        df.to_csv(csv_file, index=False)

        return {
            "base_dir": str(tmp_path),
            "jd_path": str(jd_file),
            "resume_path": str(resume_file),
            "csv_path": str(csv_file),
            "output_dir": str(outputs_dir)
        }

    def test_read_job_description_tool(self, setup_mock_dataset):
        """Ensures the file reader loads job description strings securely."""
        res = read_job_description_tool._run(jd_path=setup_mock_dataset["jd_path"])
        assert res["success"] is True
        assert "# AI Engineer Job Criteria" in res["content"]

    def test_candidate_index_lookup_tool_success(self, setup_mock_dataset):
        """Validates that the indexing engine matches candidate IDs with the correct filenames."""
        res = candidate_index_lookup_tool._run(
            candidate_id="CAND-TEST-01", 
            csv_path=setup_mock_dataset["csv_path"]
        )
        assert res["found"] is True
        assert res["candidate_name"] == "Alice Tester"
        assert res["resume_file"] == "resume_mock_01.md"

    def test_save_report_tool_saves_properly(self, setup_mock_dataset):
        """Validates that the export utility writes JSON data structurally to the local disk."""
        mock_data = {"candidate_id": "CAND-TEST-01", "status": "Verified"}
        res = save_report_tool._run(
            candidate_id="CAND-TEST-01", 
            report_data=mock_data, 
            output_dir=setup_mock_dataset["output_dir"]
        )
        
        assert res["success"] is True
        assert os.path.exists(res["saved_path"])
   
        with open(res["saved_path"], "r", encoding="utf-8") as f:
            saved_json = json.load(f)
        assert saved_json["status"] == "Verified"
