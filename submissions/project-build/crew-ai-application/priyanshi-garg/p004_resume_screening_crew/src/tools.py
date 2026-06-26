from crewai.tools import tool
import os

@tool
def read_job_description_tool(jd_path: str) -> dict:
    """Reads the content of a job description file carefully."""
    try:
        with open(jd_path.strip(), "r", encoding="utf-8") as f:
            return {
                "success": True,
                "content": f.read(),
                "source_file": os.path.basename(jd_path)
            }
    except Exception as e:
        return {
            "success": False,
            "content": f"Error: {str(e)}",
            "source_file": os.path.basename(jd_path)
        }

#read_resume_tool
@tool
def read_resume_tool(resume_path: str) -> dict:
    """Reads the content of a specified candidate resume file."""
    try:
        with open(resume_path.strip(), "r", encoding="utf-8") as f:
            return {
                "success": True,
                "content": f.read(),
                "source_file": os.path.basename(resume_path)
            }
    except Exception as e:
        return {
            "success": False,
            "content": f"Error: {str(e)}",
            "source_file": os.path.basename(resume_path)
        }


@tool
def candidate_index_lookup_tool(candidate_id: str) -> dict:
    """Finds the resume file for any candidate ID by scanning the folder."""
    folder = "data/p004_resume_screening_crew_dataset/resumes"
    
    num = "".join(c for c in candidate_id if c.isdigit())
    
    if num and os.path.exists(folder):
        for file in os.listdir(folder):
            if file.startswith(f"candidate_{num}_"):
                name = file.replace(f"candidate_{num}_", "").replace(".md", "")
                name = name.replace("_", " ").title()
                
                return {
                    "found": True,
                    "candidate_id": candidate_id,
                    "candidate_name": name,
                    "resume_file": file
                }
                
    return {"found": False, "message": "Candidate ID not found."}


import json

@tool
def load_screening_rubric_tool() -> dict:
    """Loads the candidate scoring rubric JSON file."""
    path = "metadata/screening_rubric.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {
            "error": f"Failed to load rubric: {str(e)}"
        }

@tool
def skill_matcher_tool(jd_skills: list, candidate_skills: list) -> dict:
    """Compares job description skills with candidate resume skills to calculate alignment."""
    jd_skills_clean = [s.strip().lower() for s in jd_skills if s.strip()]
    cand_skills_clean = [s.strip().lower() for s in candidate_skills if s.strip()]
    
    matched_skills = []
    partial_matches = []
    missing_skills = []
    
    used_cand_skills = set()
    
    for jd_skill in jd_skills_clean:
        orig_jd_skill = next(s for s in jd_skills if s.strip().lower() == jd_skill)
        
        if jd_skill in cand_skills_clean:
            matched_skills.append(orig_jd_skill)
            used_cand_skills.add(jd_skill)
            continue
            
        is_partial = False
        for cand_skill in cand_skills_clean:
            if cand_skill in used_cand_skills:
                continue
            if jd_skill in cand_skill or cand_skill in jd_skill:
                partial_matches.append(orig_jd_skill)
                used_cand_skills.add(cand_skill)
                is_partial = True
                break
                
        if not is_partial:
            missing_skills.append(orig_jd_skill)
            
    total_jd_skills = len(jd_skills_clean)
    if total_jd_skills > 0:
        match_score = len(matched_skills) + (len(partial_matches) * 0.5)
        match_percentage = (match_score / total_jd_skills) * 100
        match_percentage = int(match_percentage) if match_percentage.is_integer() else round(match_percentage, 1)
    else:
        match_percentage = 0
        
    return {
        "matched_skills": matched_skills,
        "partial_matches": partial_matches,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }

@tool("validate_report_schema_tool")
def validate_report_schema_tool(report_data: dict) -> dict:
    """Validates that the final screening report dictionary contains all required fields."""
    # Handle variations of the band field gracefully
    required = ["candidate_id", "candidate_name", "overall_score", "max_score", "percentage"]
    missing = [f for f in required if f not in report_data]
    
    # Check if at least one variant of recommendation is present
    if "recommendation_band" not in report_data and "recommendation" not in report_data:
        missing.append("recommendation_band")
        
    return {"schema_valid": len(missing) == 0, "missing_fields": missing}

Tools = [read_job_description_tool,
read_resume_tool,
candidate_index_lookup_tool,
load_screening_rubric_tool,
skill_matcher_tool,
validate_report_schema_tool]