import json
import os
import pandas as pd


def read_job_description_tool(path):
    try:
        with open(path, "r") as f:
            return {"success": True, "content": f.read()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def read_resume_tool(path):
    try:
        with open(path, "r") as f:
            return {"success": True, "content": f.read()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def candidate_index_lookup_tool(candidate_id, index_path):
    df = pd.read_csv(index_path)
    row = df[df["candidate_id"] == candidate_id]

    if row.empty:
        return {"found": False}

    r = row.iloc[0]
    return {
        "found": True,
        "candidate_id": r["candidate_id"],
        "candidate_name": r["candidate_name"],
        "resume_file": r["resume_file"]
    }


def load_screening_rubric_tool(path):
    with open(path, "r") as f:
        return json.load(f)


def score_calculator_tool(category_scores):
    total = sum(category_scores.values())
    pct = (total / 40) * 100

    if pct >= 80:
        band = "STRONG_MATCH"
    elif pct >= 60:
        band = "MODERATE_MATCH"
    elif pct >= 40:
        band = "WEAK_MATCH"
    else:
        band = "NEEDS_MANUAL_REVIEW"

    return {
        "overall_score": total,
        "max_score": 40,
        "percentage": pct,
        "recommendation_band": band
    }


def save_report_tool(report, output_path, candidate_id):
    os.makedirs(output_path, exist_ok=True)
    file_path = os.path.join(output_path, f"{candidate_id}_screening_report.json")

    with open(file_path, "w") as f:
        json.dump(report, f, indent=2)

    return file_path