import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools import validate_report

def test_report_recommendation_matches_score_band():
    outputs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../outputs"))
    assert os.path.exists(outputs_dir)
    
    report_files = [f for f in os.listdir(outputs_dir) if f.endswith("_screening_report.json")]
    assert len(report_files) > 0
    
    for filename in report_files:
        filepath = os.path.join(outputs_dir, filename)
        report = validate_report(filepath)
        assert isinstance(report, dict) and "valid" not in report
        
        percentage = report.get("percentage")
        recommendation = report.get("recommendation")
        
        assert percentage is not None
        assert recommendation is not None
        
        if percentage >= 80:
            assert recommendation == "STRONG_MATCH"
        elif percentage >= 60:
            assert recommendation == "MODERATE_MATCH"
        elif percentage >= 40:
            assert recommendation == "WEAK_MATCH"
        else:
            assert recommendation == "NEEDS_MANUAL_REVIEW"