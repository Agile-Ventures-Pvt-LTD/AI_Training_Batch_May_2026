import pytest
import json
from pathlib import Path
from src.tools import read_job_description_tool, candidate_index_lookup_tool, read_resume_tool
from src.scoring import score_candidate, get_recommendation_band
from src.output_writer import make_report
from src.tools import validate_report_schema_tool, save_report_tool


def load_report(candidate_id):
    path = Path("outputs") / f"{candidate_id}_screening_report.json"
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None

def test_report_recommendation_matches_score_band():
    cand_ids = ["CAND-001", "CAND-002", "CAND-003"]
    for cid in cand_ids:
        lookup = candidate_index_lookup_tool(cid)
        resume = read_resume_tool(lookup["resume_file"])
        scores = score_candidate(resume["content"])
        pct = scores["percentage"]
        band = scores["recommendation_band"]

        if pct >= 80:
            assert band == "STRONG_MATCH"
        elif pct >= 60:
            assert band == "MODERATE_MATCH"
        elif pct >= 40:
            assert band == "WEAK_MATCH"
        else:
            assert band == "NEEDS_MANUAL_REVIEW"


