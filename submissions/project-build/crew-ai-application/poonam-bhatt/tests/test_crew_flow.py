import os
import sys
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.crew import run_screening_crew

def test_run_screening_crew_fallback():
    with patch.dict(os.environ, {"GROQ_API_KEY": "..."}):
        report = run_screening_crew("CAND-001")
        assert isinstance(report, dict)
        assert report["candidate_id"] == "CAND-001"
        assert report["candidate_name"] == "Rohan Mehta"
        assert report["recommendation"] in ["STRONG_MATCH", "MODERATE_MATCH"]
        assert report["percentage"] >= 60.0
        assert "strengths" in report
        assert "interview_questions" in report

def test_run_screening_crew_invalid_candidate():
    with patch.dict(os.environ, {"GROQ_API_KEY": "..."}):
        report = run_screening_crew("CAND-UNKNOWN")
        assert isinstance(report, dict)
        assert report["candidate_id"] == "CAND-UNKNOWN"
        assert report["recommendation"] == "NEEDS_MANUAL_REVIEW"