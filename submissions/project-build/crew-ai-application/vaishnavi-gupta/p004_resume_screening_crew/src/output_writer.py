import json
from datetime import datetime
from pathlib import Path

LOG_FILE = {
    "outputs/CAND-001_screening_report.jsonl",
    "outputs/CAND-002_screening_report.jsonl",
    "outputs/CAND-003_screening_report.jsonl",
    "outputs/CAND-001_screening_report.jsonl",
    "outputs/CAND-00_screening_report.jsonl",
}


Path("outputs").mkdir(exist_ok=True)


def log_execution(
    user_query,
    tasks,
    task_results,
    final_report
):
    record = {
        "candidate_id": "",
        "candidate_name": "",
        "role_title": "",
        "overall_score": 0,
        "max_score": 40,
        "percentage": 0,
        "recommendation": "",
        "executive_summary": "",
        "strengths": [],
        "gaps": [],
        "interview_focus_areas": [],
        "interview_questions": {
        "technical_questions": [],
        "project_deep_dive_questions": [],
        "scenario_questions": [],
        "gap_validation_questions": []
 },
       "evidence": [],
        "human_review_note": ""
}
    

    print("Writing log...")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print("Log saved.")