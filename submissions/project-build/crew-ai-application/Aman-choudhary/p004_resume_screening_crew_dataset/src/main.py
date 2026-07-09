import argparse
import json
import logging
from pathlib import Path
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List
from config import (JOB_DESCRIPTION_FILE,RESUMES_DIR,)
from tools import (read_job_description_tool,read_resume_tool,candidate_index_lookup_tool,)
from output_writer import write_report
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
def generate_screening_report(candidate_id: str) -> dict:
    """
    Generate candidate report.
    """
    candidate_info = (candidate_index_lookup_tool(candidate_id))
    if not candidate_info.get("found"):
        raise ValueError(
            candidate_info.get("message","Candidate not found."))
    jd_result = read_job_description_tool(str(JOB_DESCRIPTION_FILE))
    resume_path = (RESUMES_DIR /candidate_info["resume_file"])
    resume_result = read_resume_tool(str(resume_path))
    report = {
        "candidate_id": candidate_id,
        "candidate_name": candidate_info[
            "candidate_name"
        ],
        "role_title": "AI Engineer",
        "overall_score": 0,
        "max_score": 40,
        "percentage": 0,
        "recommendation":
            "NEEDS_MANUAL_REVIEW",
        "executive_summary":
            (
                "Initial screening "
                "report generated."
            ),
        "strengths": [],
        "gaps": [],
        "interview_focus_areas": [],
        "interview_questions": {
            "technical_questions": [],
            "project_deep_dive_questions": [],
            "scenario_questions": [],
            "gap_validation_questions": []
        },
        "evidence": [
            jd_result.get(
                "source_file",
                ""
            ),
            resume_result.get(
                "source_file",
                ""
            )
        ],
        "human_review_note": (
            "This is an AI-assisted "
            "screening report based on "
            "the provided resume and "
            "job description. A human "
            "reviewer should validate "
            "the recommendation before "
            "making any recruitment "
            "decision."
        )
    }

    return report



def run_candidate_screening(candidate_id: str):
    """
    Run candidate screening.
    """
    logger.info("Processing %s",candidate_id)
    report = generate_screening_report(candidate_id)
    result = write_report(candidate_id,report)
    logger.info(result)
    return result
def run_sample_screening():
    """
    Required PRD candidates.
    """
    candidates = [
        "CAND-001",
        "CAND-002",
        "CAND-003",
    ]

    for candidate_id in candidates:
        try:
            run_candidate_screening(candidate_id)
        except Exception as exc:
            logger.error("Failed for %s: %s",candidate_id,str(exc))
def parse_args():
    parser = argparse.ArgumentParser(description="Resume Screening Crew")
    parser.add_argument("--candidate-id",type=str,help="Candidate ID")
    parser.add_argument("--run-sample-screening",action="store_true",help="Run sample screening")
    return parser.parse_args()
def main():
    args = parse_args()
    if args.candidate_id:
        run_candidate_screening(args.candidate_id)
        return
    if args.run_sample_screening:
        run_sample_screening()
        return
    print("\nUsage:\n"
        "python src/main.py "
        "--candidate-id CAND-001\n\n"
        "or\n\n"
        "python src/main.py "
        "--run-sample-screening\n")


if __name__ == "__main__":
    main()