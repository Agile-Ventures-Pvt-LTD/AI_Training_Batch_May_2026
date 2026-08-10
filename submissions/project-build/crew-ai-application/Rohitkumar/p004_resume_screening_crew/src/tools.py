import json
import csv
from typing import Dict, List
from src.config import JD_PATH, RESUMES_DIR, CANDIDATE_INDEX_PATH, OUTPUT_PATH
from src.scoring import match_skills, calculate_scores_direct, load_rubric


def read_job_description_tool() -> Dict:
    try:
        with open(JD_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        return {"success": True, "content": content, "source_file": JD_PATH.name}
    except FileNotFoundError:
        return {"success": False, "content": "", "source_file": str(JD_PATH), "error": "JD file not found"}


def read_resume_tool(resume_filename: str) -> Dict:
    try:
        resume_path = RESUMES_DIR / resume_filename
        with open(resume_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"success": True, "content": content, "source_file": resume_filename}
    except FileNotFoundError:
        return {"success": False, "content": "", "source_file": resume_filename, "error": "Resume file not found"}


def candidate_index_lookup_tool(candidate_id: str) -> Dict:
    try:
        with open(CANDIDATE_INDEX_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["candidate_id"].strip().upper() == candidate_id.strip().upper():
                    return {
                        "found": True,
                        "candidate_id": row["candidate_id"],
                        "candidate_name": row["candidate_name"],
                        "resume_file": row["resume_file"],
                        "years_experience": row.get("years_experience", ""),
                        "current_role": row.get("current_role", ""),
                        "primary_skills": row.get("primary_skills", "")
                    }
        return {"found": False, "message": "Candidate ID not found"}
    except FileNotFoundError:
        return {"found": False, "message": "Candidate index file not found"}


def load_screening_rubric_tool() -> Dict:
    try:
        rubric = load_rubric()
        return {"categories": list(rubric["categories"].keys()), "score_range": "0 to 5", "max_score": rubric["max_score"]}
    except FileNotFoundError:
        return {"categories": [], "score_range": "0 to 5", "max_score": 40}


def score_calculator_tool(category_scores: Dict[str, int]) -> Dict:
    return calculate_scores_direct(category_scores)


def save_report_tool(candidate_id: str, report: Dict) -> Dict:
    try:
        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        file_path = OUTPUT_PATH / f"{candidate_id}_screening_report.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        return {"success": True, "file_path": str(file_path)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def skill_matcher_tool(jd_skills: List[str], resume_text: str) -> Dict:
    return match_skills(jd_skills, resume_text)


def validate_report_schema_tool(report: Dict) -> Dict:
    required = ["candidate_id", "candidate_name", "role_title", "overall_score", "max_score", "percentage", "recommendation", "executive_summary", "strengths", "gaps", "interview_focus_areas", "interview_questions", "evidence", "human_review_note"]
    missing = [f for f in required if f not in report]
    return {"schema_valid": len(missing) == 0, "missing_fields": missing}


def batch_candidate_loader_tool() -> List[Dict]:
    candidates = []
    try:
        with open(CANDIDATE_INDEX_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                candidates.append(dict(row))
    except FileNotFoundError:
        pass
    return candidates