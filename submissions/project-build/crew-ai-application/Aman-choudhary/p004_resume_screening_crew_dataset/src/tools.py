import json
from pathlib import Path
from typing import Dict, List
from config import (CANDIDATE_INDEX_FILE,SCREENING_RUBRIC_FILE,SKILL_SYNONYMS_FILE,)
import pandas as pd
def read_job_description_tool(jd_path: str) -> Dict:
    """
    Read job description file.
    """
    file_path = Path(jd_path)
    if not file_path.exists():
        return {"success": False,"error": f"Job description file not found: {jd_path}"}
    try:
        content = file_path.read_text(encoding="utf-8")
        return {"success": True,"content": content,"source_file": file_path.name}
    except Exception as exc:
        return {"success": False,"error": str(exc)}
def read_resume_tool(resume_path: str) -> Dict:
    """
    Read resume markdown file.
    """
    file_path = Path(resume_path)
    if not file_path.exists():
        return {"success": False,"error": f"Resume file not found: {resume_path}"}
    try:
        content = file_path.read_text(encoding="utf-8")
        return {"success": True,"content": content,"source_file": file_path.name}
    except Exception as exc:
        return {"success": False,"error": str(exc)}
def candidate_index_lookup_tool(candidate_id: str) -> Dict:
    """
    Lookup candidate details.
    """
    try:
        df = pd.read_csv(CANDIDATE_INDEX_FILE)
        candidate = df[df["candidate_id"] == candidate_id]
        if candidate.empty:
            return {"found": False,"message": "Candidate ID not found."}
        row = candidate.iloc[0]
        return {"found": True,"candidate_id": row["candidate_id"],"candidate_name": row["candidate_name"],"resume_file": row["resume_file"]}
    except Exception as exc:
        return {"found": False,"message": str(exc)}
def load_screening_rubric_tool() -> Dict:
    """
    Load scoring rubric.
    """
    try:
        with open(SCREENING_RUBRIC_FILE,"r",encoding="utf-8") as file:
            return json.load(file)
    except Exception as exc:
        return {"success": False,"error": str(exc)}
def load_skill_synonyms_tool() -> Dict:
    """
    Load skill synonym mapping.
    """
    try:
        with open(SKILL_SYNONYMS_FILE,"r",encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}
def skill_matcher_tool(jd_skills: List[str],candidate_skills: List[str])-> Dict:
    """
    Match JD skills against resume skills.
    """
    synonyms = load_skill_synonyms_tool()
    candidate_lower = {skill.lower()for skill in candidate_skills}
    matched_skills = []
    partial_matches = []
    missing_skills = []
    for jd_skill in jd_skills:
        skill_lower = jd_skill.lower()
        if skill_lower in candidate_lower:
            matched_skills.append(jd_skill)
            continue
        synonym_match = False
        for values in synonyms.values():
            values_lower = [item.lower()for item in values]
            if (skill_lower in values_lower and any(x in candidate_lower for x in values_lower)):
                synonym_match = True
                break
        if synonym_match:
            partial_matches.append(jd_skill)
        else:
            missing_skills.append(jd_skill)
    total = len(jd_skills)
    percentage = (round(
            (
                len(matched_skills)
                + len(partial_matches)
            )
            / total * 100,
            2,
        )
        if total > 0
        else 0
    )

    return {
        "matched_skills": matched_skills,
        "partial_matches": partial_matches,
        "missing_skills": missing_skills,
        "match_percentage": percentage
    }

def validate_report_schema_tool(report: Dict) -> Dict:
    required_fields = [
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
        "human_review_note",
    ]
    missing_fields = [
        field
        for field in required_fields
        if field not in report
    ]

    return {
        "schema_valid": (
            len(missing_fields) == 0
        ),
        "missing_fields": missing_fields,
    }
def save_report_tool(report: Dict,file_path: str) -> Dict:
    """
    Save report JSON file.
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True,exist_ok=True)
        with open(path,"w",encoding="utf-8") as file:
            json.dump(report,file,indent=4,ensure_ascii=False)
        return {"success": True,"file_path": str(path)}
    except Exception as exc:
        return {"success": False,"error": str(exc)}