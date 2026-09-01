import os
import json
import csv
from typing import Dict, List
from crewai.tools import tool
from src.config import DATASET_PATH, OUTPUT_PATH
from src.scoring import calculate_score_metrics
from src.output_writer import write_json_report

def get_dataset_file_path(relative_path):
    resolved = os.path.join(DATASET_PATH, relative_path)
    if os.path.exists(resolved):
        return resolved
    return relative_path if os.path.exists(relative_path) else resolved

@tool("read_job_description_tool")
def read_job_description_tool(jd_path):
    """
    Reads the job description file.
    Input: jd_path
    Output: Dictionary with success, content and source_file
    """
    jd_path=get_dataset_file_path(jd_path)
    if not os.path.exists(jd_path):
        return {
                "success": False,
                "error": f"Job description file not found",
                "content": ""}
    with open(jd_path, "r", encoding="utf-8") as f:
        content = f.read()
        return {
            "success": True,
            "content": content,
            "source_file": os.path.basename(jd_path)}
            
@tool("read_resume_tool")
def read_resume_tool(resume_path):
    """
    Reads a candidate resume file
    Input: resume_path
    Output: Dictionary with success, content and source_file
    """
    resume_path=get_dataset_file_path(resume_path)
    if not os.path.exists(resume_path):
        return {
                "success": False,
                "error": f"Resume file not found",
                "content": ""}
    with open(resume_path, "r", encoding="utf-8") as f:
        content = f.read()
        return {
            "success": True,
            "content": content,
            "source_file": os.path.basename(resume_path)}
    
@tool("candidate_index_lookup_tool")
def candidate_index_lookup_tool(candidate_id):
    """
    Finds the resume file and metadata for a candidate ID.
    Input: candidate_id 
    Output: Dictionary with candidate details if found
    """
    csv_path = get_dataset_file_path("metadata/candidate_index.csv")
    
    if not os.path.exists(csv_path):
            return {
                "found": False,
                "message": f"Candidate index CSV file not found"
            }
        
    with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("candidate_id").strip() == candidate_id.strip():
                    return {
                        "found": True,
                        "candidate_id": row.get("candidate_id"),
                        "candidate_name": row.get("candidate_name"),
                        "resume_file": row.get("resume_file"),
                        "years_experience": row.get("years_experience"),
                        "current_role": row.get("current_role"),
                        "primary_skills": row.get("primary_skills")
                    }
        
    return {
            "found": False,
            "message": "Candidate ID was not found."
        }

@tool("load_screening_rubric_tool")
def load_screening_rubric_tool(dummy: str = ""):
    """
     Loads the scoring rubric from: metadata/screening_rubric.json
     Output: Dictionary of categories, score range and maximum score
    """
    rubric_path = get_dataset_file_path("metadata/screening_rubric.json")
    
    if not os.path.exists(rubric_path):
        return {
                "success": False,
                "error": f"Screening rubric file not found"
            }
    with open(rubric_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

@tool("score_calculator_tool")
def score_calculator_tool(category_scores):
    """
    Calculates total score, percentage, and recommendation band.
    Input: category_scores
    Output: Dictionary containing overall_score, max_score, percentage and recommendation bands
    """
    cleaned_scores = {}
    for k, v in category_scores.items():
        cleaned_scores[k] = int(v)
    return calculate_score_metrics(cleaned_scores)
    
@tool("save_report_tool")
def save_report_tool(candidate_id, report_data):
    """
    Saves the final report to the outputs/ folder.
    Input: candidate_id and report_data
    Output: Dictionary showing success and output path
    """
    clean_id = candidate_id.strip()
    json_path = write_json_report(clean_id, report_data, OUTPUT_PATH)
    # md_path = write_markdown_report(clean_id, report_data, OUTPUT_PATH)
    return {
            "success": True,
            "json_path": json_path,
            # "markdown_path": md_path,
            "message": f"Reports are saved"
        }

@tool("skill_matcher_tool")
def skill_matcher_tool(jd_skills, candidate_skills):
    """
    Compares JD skills with candidate resume skills.
    Input: jd_skills and candidate_skills
    Output: Dictionary with matched_skills, partial_matches, missing_skills, match_percentage
    """
    synonyms_path = get_dataset_file_path("metadata/skill_synonyms.json")
    synonyms = {}
    with open(synonyms_path, "r", encoding="utf-8") as f:
        synonyms = json.load(f)
                
    def get_normalized_skill(skill):
            skill = skill.strip().lower()
            for key, syn_list in synonyms.items():
                if skill == key or skill in [s.lower() for s in syn_list]:
                    return key
            return skill
    norm_jd = {}
    for s in jd_skills:
        norm_jd[get_normalized_skill(s)] = s
    norm_cand = set(get_normalized_skill(s) for s in candidate_skills)
        
    matched_skills = []
    partial_matches = []
    missing_skills = []
    for norm_s, original_s in norm_jd.items():
            if norm_s in norm_cand:
                matched_skills.append(original_s)
            else:
                is_partial = False
                for cand_s in norm_cand:
                    if norm_s in cand_s or cand_s in norm_s:
                        partial_matches.append(original_s)
                        is_partial = True
                        break
                if not is_partial:
                    missing_skills.append(original_s)
                    
    total_jd = len(jd_skills)
    match_pct = (len(matched_skills) / total_jd * 100) if total_jd > 0 else 0.0
    return {
            "matched_skills": matched_skills,
            "partial_matches": partial_matches,
            "missing_skills": missing_skills,
            "match_percentage": round(match_pct, 2)
        }

@tool("validate_report_schema_tool")
def validate_report_schema_tool(report_data):
    """
    Validates that the final report contains all required fields.
    Input: report_data
    Output: Dictionary with schema_valid and missing_fields
    """
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
        "interview_questions"
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in report_data:
            missing_fields.append(field)
            
    if "interview_questions" in report_data:
        iq = report_data["interview_questions"]
        inner_fields = [
            "technical_questions",
            "project_deep_dive_questions",
            "scenario_questions",
            "gap_validation_questions"
        ]
        for inner in inner_fields:
            if not isinstance(iq, dict) or inner not in iq:
                missing_fields.append(f"interview_questions.{inner}")
                
    return {
        "schema_valid": len(missing_fields) == 0,
        "missing_fields": missing_fields
    }

    