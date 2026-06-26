import os
import json
import csv
from typing import Optional
from crewai.tools import tool
from scoring import calculate_score, SCORE_CATEGORIES
from config import (
    JD_PATH,
    RESUMES_PATH,
    CANDIDATE_INDEX_PATH,
    SCREENING_RUBRIC_PATH,
    SKILL_SYNONYMS_PATH,
    OUTPUT_PATH,
)


@tool("read_job_description_tool")
def read_job_description_tool(jd_path: str = JD_PATH) -> dict:
    """
    Reads the job description file and returns its full raw content.
    Use this first before doing any analysis. The content contains the role title,
    required skills, preferred skills, responsibilities, and experience expectations.
    Extract all of these carefully from the returned content.
    """
    try:
        with open(jd_path, "r", encoding="utf-8") as f:
            return {"success": True, "content": f.read(), "source_file": os.path.basename(jd_path)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool("read_resume_tool")
def read_resume_tool(resume_path: str) -> dict:
    """
    Reads a candidate resume file and returns its full raw content.
    The content will contain the candidate's skills, projects, work experience,
    education, and certifications. Extract all structured information from it carefully.
    Do not infer or hallucinate skills or experience that are not explicitly present.
    """
    try:
        with open(resume_path, "r", encoding="utf-8") as f:
            return {"success": True, "content": f.read(), "source_file": os.path.basename(resume_path)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool("candidate_index_lookup_tool")
def candidate_index_lookup_tool(candidate_id: str) -> dict:
    """
    Looks up a candidate by their ID (e.g. CAND-001) in the candidate index
    and returns their name and resume file path. Always use this before reading
    a resume so you have the correct file path for that candidate.
    """
    try:
        with open(CANDIDATE_INDEX_PATH, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["candidate_id"].strip() == candidate_id.strip():
                    resume_file = row["resume_file"].strip()
                    return {
                        "found": True,
                        "candidate_id": row["candidate_id"].strip(),
                        "candidate_name": row["candidate_name"].strip(),
                        "resume_file": resume_file,
                        "resume_path": os.path.join(RESUMES_PATH, resume_file),
                    }
        return {"found": False, "message": f"Candidate ID not found: {candidate_id}"}
    except Exception as e:
        return {"found": False, "error": str(e)}


@tool("load_screening_rubric_tool")
def load_screening_rubric_tool(dummy: Optional[str] = None) -> dict:
    """
    Loads the scoring rubric and skill synonyms. Returns the 8 scoring categories,
    their score range (0-5), and synonym mappings to help normalize skill names.
    Use the synonyms to match variations like 'FastAPI' to 'api', or 'LangChain'
    to 'agent_frameworks' when scoring a candidate.
    """
    try:
        with open(SCREENING_RUBRIC_PATH, "r", encoding="utf-8") as f:
            rubric = json.load(f)
        with open(SKILL_SYNONYMS_PATH, "r", encoding="utf-8") as f:
            synonyms = json.load(f)
        return {
            "success": True,
            "rubric": rubric,
            "categories": SCORE_CATEGORIES,
            "score_range": "0 to 5 per category, 40 max total",
            "skill_synonyms": synonyms,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool("skill_matcher_tool")
def skill_matcher_tool(jd_skills_json: str, candidate_skills_json: str) -> dict:
    """
    Compares the job description's required skills against the candidate's skills.
    Loads synonym mappings to normalize skill names before comparing — so 'FastAPI'
    matches 'api', 'LangChain' matches 'agent_frameworks', etc.
    Returns matched skills, partial matches, missing skills, and a match percentage.
    Use this output to justify category scores and identify gaps for interview questions.
    Pass jd_skills_json and candidate_skills_json as JSON arrays, e.g. '["python", "sql"]'.
    """
    try:
        jd_skills = json.loads(jd_skills_json)
        candidate_skills = json.loads(candidate_skills_json)
        with open(SKILL_SYNONYMS_PATH, "r", encoding="utf-8") as f:
            synonyms = json.load(f)

        def normalize(skill):
            s = skill.lower().strip()
            for canonical, variants in synonyms.items():
                if s == canonical or s in [v.lower() for v in variants]:
                    return canonical
            return s

        norm_jd = [normalize(s) for s in jd_skills]
        norm_candidate = [normalize(s) for s in candidate_skills]

        matched = [s for s in norm_jd if s in norm_candidate]
        missing = [s for s in norm_jd if s not in norm_candidate]
        partial = [s for s in norm_candidate if s not in norm_jd]
        match_pct = round(len(matched) / len(norm_jd) * 100, 2) if norm_jd else 0

        return {"matched_skills": matched, "partial_matches": partial, "missing_skills": missing, "match_percentage": match_pct}
    except Exception as e:
        return {"error": str(e)}


@tool("score_calculator_tool")
def score_calculator_tool(category_scores_json: str) -> dict:
    """
    Takes a JSON object of category scores (each 0-5) across all 8 rubric categories and
    calculates the overall score out of 40, percentage, and recommendation band.
    Bands: STRONG_MATCH (>=80%), MODERATE_MATCH (>=60%), WEAK_MATCH (>=40%),
    NEEDS_MANUAL_REVIEW (<40%). Always run this after assigning category scores
    to get the final recommendation band — do not calculate this yourself.
    Pass category_scores_json as a JSON object string, e.g. '{"python": 4, "ml": 3}'.
    """
    try:
        category_scores = json.loads(category_scores_json)
        return calculate_score(category_scores)
    except Exception as e:
        return {"error": str(e)}


@tool("validate_report_schema_tool")
def validate_report_schema_tool(report_json: str) -> dict:
    """
    Validates the final screening report has all required fields before saving.
    Checks for: candidate_id, candidate_name, role_title, overall_score, max_score,
    percentage, recommendation, executive_summary, strengths, gaps,
    interview_focus_areas, interview_questions (with technical_questions,
    project_deep_dive_questions, scenario_questions, gap_validation_questions),
    evidence, and human_review_note. Returns schema_valid and any missing fields.
    Fix all missing fields before calling save_report_tool.
    Pass report_json as a JSON object string.
    """
    try:
        report = json.loads(report_json)
    except Exception as e:
        return {"schema_valid": False, "missing_fields": [], "error": f"Invalid JSON: {e}"}

    required = [
        "candidate_id", "candidate_name", "role_title", "overall_score",
        "max_score", "percentage", "recommendation", "executive_summary",
        "strengths", "gaps", "interview_focus_areas", "interview_questions",
        "evidence", "human_review_note",
    ]
    required_iq = ["technical_questions", "project_deep_dive_questions", "scenario_questions", "gap_validation_questions"]

    missing = [f for f in required if f not in report]
    missing += [f"interview_questions.{f}" for f in required_iq if f not in report.get("interview_questions", {})]

    return {"schema_valid": len(missing) == 0, "missing_fields": missing}


@tool("save_report_tool")
def save_report_tool(candidate_id: str, report_json: str) -> dict:
    """
    Saves the final validated screening report as a JSON file to the outputs folder.
    The file will be saved as outputs/<candidate_id>_screening_report.json.
    Only call this after validate_report_schema_tool confirms schema_valid is True.
    Always include the human_review_note: 'This is an AI-assisted screening report
    based on the provided resume and job description. A human reviewer should
    validate the recommendation before making any recruitment decision.'
    Pass report_json as a JSON object string.
    """
    try:
        report = json.loads(report_json)
        os.makedirs(OUTPUT_PATH, exist_ok=True)
        path = os.path.join(OUTPUT_PATH, f"{candidate_id}_screening_report.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        return {"success": True, "saved_to": path}
    except Exception as e:
        return {"success": False, "error": str(e)}