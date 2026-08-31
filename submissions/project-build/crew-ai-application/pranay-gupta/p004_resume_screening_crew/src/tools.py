import os
import json
import csv
from crewai.tools import tool
from src.config import DATASET_PATH, OUTPUT_PATH

DATASET_BASE = str(DATASET_PATH)
OUTPUT_BASE = str(OUTPUT_PATH)

@tool("read_job_description_tool")
def read_job_description_tool(jd_path: str) -> str:
    """Reads the job description file from disk."""
    try:
        with open(jd_path, "r", encoding="utf-8") as f:
            return json.dumps({"success": True, "content": f.read(), "source_file": os.path.basename(jd_path)})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool("read_resume_tool")
def read_resume_tool(resume_path: str) -> str:
    """Reads a candidate resume file from disk."""
    try:
        with open(resume_path, "r", encoding="utf-8") as f:
            return json.dumps({"success": True, "content": f.read(), "source_file": os.path.basename(resume_path)})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool("candidate_index_lookup_tool")
def candidate_index_lookup_tool(candidate_id: str) -> str:
    """Finds the candidate's resume filename from the metadata index file using candidate_id."""
    csv_path = os.path.join(DATASET_BASE, "metadata/candidate_index.csv")
    try:
        if not os.path.exists(csv_path):
            return json.dumps({"found": False, "message": f"Index file not found at {csv_path}"})
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("candidate_id") == candidate_id:
                    return json.dumps({
                        "found": True,
                        "candidate_id": row["candidate_id"],
                        "candidate_name": row["candidate_name"],
                        "resume_file": row["resume_file"]
                    })
        return json.dumps({"found": False, "message": "Candidate ID not found."})
    except Exception as e:
        return json.dumps({"found": False, "message": str(e)})

@tool("load_screening_rubric_tool")
def load_screening_rubric_tool() -> str:
    """Loads the core grading matrix categories from screening_rubric.json."""
    rubric_path = os.path.join(DATASET_BASE, "metadata/screening_rubric.json")
    try:
        with open(rubric_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data)
    except Exception:
        return json.dumps({
            "categories": ["python_programming", "sql_database_skills", "api_integration", 
                           "llm_application_development", "agent_frameworks", "rag_understanding", 
                           "testing_and_quality", "communication"],
            "score_range": "0 to 5", "max_score": 40
        })

@tool("score_calculator_tool")
def score_calculator_tool(category_scores: dict) -> str:
    """Calculates overall score, percentage, and assigns the correct recommendation band."""
    try:
        valid_cats = ["python_programming", "sql_database_skills", "api_integration", 
                      "llm_application_development", "agent_frameworks", "rag_understanding", 
                      "testing_and_quality", "communication"]
        cleaned_scores = {k: int(v) for k, v in category_scores.items() if k in valid_cats}
        
        for cat in valid_cats:
            if cat not in cleaned_scores:
                cleaned_scores[cat] = 0
                
        overall_score = sum(cleaned_scores.values())
        max_score = 40
        percentage = (overall_score / max_score) * 100
        
        if percentage >= 80:
            band = "STRONG_MATCH"
        elif percentage >= 60:
            band = "MODERATE_MATCH"
        elif percentage >= 40:
            band = "WEAK_MATCH"
        else:
            band = "NEEDS_MANUAL_REVIEW"
            
        return json.dumps({
            "overall_score": overall_score,
            "max_score": max_score,
            "percentage": round(percentage, 2),
            "recommendation_band": band,
            "category_scores": cleaned_scores
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool("save_report_tool")
def save_report_tool(candidate_id: str, report_json_str: str) -> str:
    """Saves the finalized report dictionary cleanly inside the configured outputs/ directory."""
    try:
        os.makedirs(OUTPUT_BASE, exist_ok=True)
        filename = f"{candidate_id}_screening_report.json"
        full_path = os.path.join(OUTPUT_BASE, filename)
        
        data = json.loads(report_json_str) if isinstance(report_json_str, str) else report_json_str
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return json.dumps({"success": True, "saved_path": full_path})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool("skill_matcher_tool")
def skill_matcher_tool(jd_skills: list, resume_skills: list) -> str:
    """Cross references technical terms using multi-mapping aliases from skill_synonyms.json."""
    syn_path = os.path.join(DATASET_BASE, "metadata/skill_synonyms.json")
    synonyms = {}
    if os.path.exists(syn_path):
        try:
            with open(syn_path, "r", encoding="utf-8") as f:
                synonyms = json.load(f)
        except Exception:
            pass

    matched, partial, missing = [], [], []
    res_skills_lower = [str(s).lower().strip() for s in resume_skills]
    
    for skill in jd_skills:
        skill_lower = str(skill).lower().strip()
        if skill_lower in res_skills_lower:
            matched.append(skill)
            continue
            
        found_syn = False
        for master, aliases in synonyms.items():
            if skill_lower == master.lower() or skill_lower in [a.lower() for a in aliases]:
                if any(a.lower() in res_skills_lower for a in aliases) or master.lower() in res_skills_lower:
                    partial.append(skill)
                    found_syn = True
                    break
        if not found_syn:
            missing.append(skill)
            
    total = len(jd_skills) if jd_skills else 1
    pct = ((len(matched) + len(partial)) / total) * 100
    return json.dumps({
        "matched_skills": matched,
        "partial_matches": partial,
        "missing_skills": missing,
        "match_percentage": round(pct, 2)
    })

@tool("validate_report_schema_tool")
def validate_report_schema_tool(report_json_str: str) -> str:
    """Validates that a generated screening report matches the final output structure constraints."""
    required_keys = ["candidate_id", "candidate_name", "role_title", "overall_score", 
                     "max_score", "percentage", "recommendation", "executive_summary", 
                     "strengths", "gaps", "interview_focus_areas", "interview_questions"]
    try:
        data = json.loads(report_json_str) if isinstance(report_json_str, str) else report_json_str
        missing = [k for k in required_keys if k not in data]
        return json.dumps({"schema_valid": len(missing) == 0, "missing_fields": missing})
    except Exception as e:
        return json.dumps({"schema_valid": False, "error": str(e)})