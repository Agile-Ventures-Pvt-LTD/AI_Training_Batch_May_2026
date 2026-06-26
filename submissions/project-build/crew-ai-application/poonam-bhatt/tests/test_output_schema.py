import os
import sys
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools import validate_report
from src.schemas import ScreeningReport

def test_generated_reports_conformance():
    outputs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../outputs"))
    if not os.path.exists(outputs_dir):
        pytest.skip("outputs/ directory does not exist")
        
    report_files = [f for f in os.listdir(outputs_dir) if f.endswith("_screening_report.json")]
    if not report_files:
        pytest.skip("No report files found")
        
    for filename in report_files:
        filepath = os.path.join(outputs_dir, filename)
        validated = validate_report(filepath)
        assert isinstance(validated, dict) and "valid" not in validated
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        try:
            if "interview_question" in data and "interview_questions" not in data:
                data["interview_questions"] = data["interview_question"]
            elif "interview_questions" in data and "interview_question" not in data:
                data["interview_question"] = data["interview_questions"]
                
            report_obj = ScreeningReport(**data)
            assert report_obj.candidate_id is not None
            assert report_obj.max_score == 40
        except Exception as e:
            pytest.fail(f"Report {filename} failed Pydantic schema validation: {e}")
