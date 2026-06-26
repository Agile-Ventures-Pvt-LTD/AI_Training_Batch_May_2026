import os
import json
from datetime import datetime
from typing import List, Dict, Any, Union

REQUIRED_FIELDS = [
    "candidate_id",
    "candidate_name",
    "role_title",
    "overall_score",
    "max_score",
    "percentage",
    "recommendation",
    "executive_summary",
    "strengths",
    "gaps",
    "interview_focus_areas",
    "interview_questions",
    "evidence",
    "human_review_note"
]

def read_job_description_tool(jd_path: str) -> Dict[str, Any]:
    response = {
        "success": False,
        "content": "",
        "source_file": ""
    }
    if os.path.exists(jd_path) and os.path.isfile(jd_path):
        try:
            with open(jd_path, 'r', encoding='utf-8') as file:
                content = file.read()
            response["success"] = True
            response["content"] = content
            response["source_file"] = os.path.basename(jd_path)
        except Exception as e:
            response["content"] = f"Error reading file: {str(e)}"
    else:
        fallback_path = os.path.join("data", "p004_resume_screening_crew_dataset", "job_description", "jd_ai_engineer.md")
        if os.path.exists(fallback_path):
            try:
                with open(fallback_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                response["success"] = True
                response["content"] = content
                response["source_file"] = os.path.basename(fallback_path)
            except Exception as e:
                response["content"] = f"Error reading fallback file: {str(e)}"
        else:
            response["content"] = f"File does not exist: {jd_path}"
    return response

def read_resume_tool(resume_path: str) -> str:
    if not os.path.exists(resume_path):
        filename = os.path.basename(resume_path)
        fallback_dir = os.path.join("data", "p004_resume_screening_crew_dataset", "resumes")
        fallback_path = os.path.join(fallback_dir, filename)
        if os.path.exists(fallback_path):
            resume_path = fallback_path
        else:
            found = False
            for root, dirs, files in os.walk("."):
                if filename in files:
                    resume_path = os.path.join(root, filename)
                    found = True
                    break
            if not found:
                raise FileNotFoundError(f"Resume file not found: {resume_path}")
    try:
        with open(resume_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                raise ValueError("Resume file is empty")
            return content
    except Exception as e:
        raise ValueError(f"Error reading resume file: {e}")

def find_resume(candidate_id: str, search_directory: str = 'resumes') -> List[str]:
    matching_files = []
    dirs_to_search = [
        search_directory,
        os.path.join("data", "p004_resume_screening_crew_dataset", "resumes"),
        "data",
        "."
    ]
    seen = set()
    for directory in dirs_to_search:
        if not os.path.exists(directory):
            continue
        for root, dirs, files in os.walk(directory):
            if ".venv" in root or "venv" in root:
                continue
            for file in files:
                norm_cid = candidate_id.lower().replace("-", "_")
                norm_cid_short = norm_cid.split("_")[-1] if "_" in norm_cid else norm_cid
                if (candidate_id.lower() in file.lower() or norm_cid in file.lower() or norm_cid_short in file.lower()) and file.endswith(".md"):
                    full_path = os.path.abspath(os.path.join(root, file))
                    if full_path not in seen:
                        seen.add(full_path)
                        rel_path = os.path.relpath(full_path, os.getcwd())
                        matching_files.append(rel_path)
    return matching_files

def calculate_score(scores: Dict[str, Any], weights: Dict[str, float] = None) -> Union[float, Dict[str, Any]]:
    categories = [
        "python_programming",
        "sql_database_skills",
        "api_integration",
        "llm_application_development",
        "agent_frameworks",
        "rag_understanding",
        "testing_and_quality",
        "communication"
    ]
    valid_scores = {}
    for cat in categories:
        val = scores.get(cat, 0)
        if isinstance(val, str):
            if "-" in val:
                val = val.split("-")[-1]
            if "/" in val:
                val = val.split("/")[0]
        try:
            val = int(float(val))
        except (ValueError, TypeError):
            val = 0
        if val < 0:
            val = 0
        elif val > 5:
            val = 5
        valid_scores[cat] = val
        
    overall_score = sum(valid_scores.values())
    max_score = 40
    percentage = (overall_score / max_score) * 100
    
    if percentage >= 80:
        recommendation = "STRONG_MATCH"
    elif percentage >= 60:
        recommendation = "MODERATE_MATCH"
    elif percentage >= 40:
        recommendation = "WEAK_MATCH"
    else:
        recommendation = "NEEDS_MANUAL_REVIEW"
        
    return {
        "scores": valid_scores,
        "overall_score": overall_score,
        "max_score": max_score,
        "percentage": percentage,
        "recommendation": recommendation
    }

def skill_matcher(job_skills: List[str], candidate_skills: List[str]) -> Dict[str, Any]:
    job_skills_set = set([skill.strip().lower() for skill in job_skills])
    candidate_skills_set = set([skill.strip().lower() for skill in candidate_skills])
    matched = list(job_skills_set & candidate_skills_set)
    partial_matches = list(candidate_skills_set - job_skills_set)
    missing = list(job_skills_set - candidate_skills_set)
    match_percentage = round((len(matched) / len(job_skills_set)) * 100, 2) if job_skills_set else 0
    return {
        "matched_skills": [skill.capitalize() for skill in matched],
        "partial_matches": [skill.capitalize() for skill in partial_matches],
        "missing_skills": [skill.capitalize() for skill in missing],
        "match_percentage": match_percentage
    }

def save_report_tool(report_content: str, report_name: str = "final_report") -> str:
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    try:
        data = json.loads(report_content)
        filename = f"{report_name}.json"
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return file_path
    except Exception:
        pass
    filename = f"{report_name}.txt"
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    return file_path

def validate_report(report: Any) -> Dict[str, Any]:
    if isinstance(report, str):
        if not os.path.exists(report):
            fallback = os.path.join("outputs", os.path.basename(report))
            if os.path.exists(fallback):
                report = fallback
            else:
                return {"valid": False, "missing_fields": REQUIRED_FIELDS, "error": f"File not found: {report}"}
        try:
            with open(report, "r", encoding="utf-8") as f:
                report = json.load(f)
        except Exception as e:
            return {"valid": False, "missing_fields": REQUIRED_FIELDS, "error": f"Failed to parse JSON: {e}"}

    if not isinstance(report, dict):
        return {"valid": False, "missing_fields": REQUIRED_FIELDS, "error": "Report must be a dictionary or a valid path to JSON"}

    if "interview_question" in report and "interview_questions" not in report:
        report["interview_questions"] = report["interview_question"]
    elif "interview_questions" in report and "interview_question" not in report:
        report["interview_question"] = report["interview_questions"]

    missing_fields = [field for field in REQUIRED_FIELDS if field not in report]
    if missing_fields:
        return {"valid": False, "missing_fields": missing_fields}
    return report

class LoadScreeningRubric:
    def __init__(self, rubric_criteria=None):
        self.rubric_criteria = rubric_criteria or {}

    def evaluate(self, load_data):
        return load_data
