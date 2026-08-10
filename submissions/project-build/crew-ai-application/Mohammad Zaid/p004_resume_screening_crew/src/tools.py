# tools.py

from pathlib import Path
from crewai.tools import tool
import csv
import json
from pydantic import BaseModel, Field

@tool("read_job_description_tool")
def read_job_description_tool(x_input: str = ""): 
    """Reads the job description file."""
    print("---calling read_job_description_tool()---\n")
    
    jd_description = None
    jd_path = Path("data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md")
    try:
        with open(jd_path, "r", encoding="utf-8") as jd:
            jd_description = jd.read()
    except Exception as err:
        print(f"Error opening file {err}")
        
    if not jd_description:
        return "Job Description not Available"
    else:
        return jd_description

    
@tool("read_resume_tool")
def read_resume_tool(res_path:str):
    """
    Reads a candidate resume file.

    """
    print("---calling read_resume_tool()---\n")
    
    resume_path=Path(f"data/p004_resume_screening_crew_dataset/resumes/{res_path}")
    try:
        with open(resume_path, mode="r") as res:
            resume_description = res.read()
    except Exception as err:
        print(f"Error openning file {res_path} {err}")
        
    if not resume_description:
        return "Job Description not Available"
    else:
        return resume_description
    



@tool("candidate_index_lookup_tool")
def candidate_index_lookup_tool(candidate_id: str) -> str:
    """
    Finds the resume file for a candidate ID.
    """
    print("---calling candidate_index_lookup_tool()---\n")
    
    cnd_idex_path = Path("data/p004_resume_screening_crew_dataset/metadata/candidate_index.csv")
    
    try:
        with open(cnd_idex_path, mode="r", encoding="utf-8") as file:
            id_file = csv.DictReader(file)
            
            for row in id_file:
                if row["candidate_id"] == candidate_id:
                    return {
                        "found": True,
                        "candidate_id": row["candidate_id"],
                        "candidate_name": row["candidate_name"],
                        "resume_file": row["resume_file"]
                    }
                    
    except Exception as err:
        print(f"Error opening file for candidate ID:{candidate_id} {err}")
        
    return {"found": False, "message": "Candidate ID not found."}


@tool("load_screening_rubric_tool")
def load_screening_rubric_tool(y_input: str = ""):
    """Loads the scoring rubric from the metadata folder."""
    print("---calling load_screening_rubric_tool()---\n")
    
    rubric_path = Path("data/p004_resume_screening_crew_dataset/metadata/screening_rubric.json")
    try:
        with open(rubric_path, mode="r", encoding="utf-8") as file:
            data = json.load(file)
        return {
            "categories": list(data["categories"].keys()),
            "score_range": f"{data['score_range']['min']} to {data['score_range']['max']}",
            "max_score": data["max_score"]
        }
    except Exception as err:
        return {"error": f"Failed to load rubric: {err}"}



class CategoryScoresInput(BaseModel):
    category_scores: str = Field(
        description="A JSON string of the 8 category scores. Example: '{\"python_programming\": 4, \"sql_database_skills\": 3...}'"
    )

@tool("score_calculator_tool")
def score_calculator_tool(category_scores: str) -> str: 
    """Calculates total score, percentage, and recommendation band from category scores."""
    print("---calling score_calculator_tool()---\n")
    
    try:
        scores_dict = json.loads(category_scores.replace("'", '"'))
    except Exception as e:
        return f"Error parsing scores: {e}"
    
    max_score = 40
    overall_score = sum(scores_dict.values())
    percentage = (overall_score / max_score) * 100
    
    if percentage >= 80:
        band = "STRONG_MATCH"
    elif percentage >= 60:
        band = "MODERATE_MATCH"
    elif percentage >= 40:
        band = "WEAK_MATCH"
    else:
        band = "NEEDS_MANUAL_REVIEW"
        
    return {
        "overall_score": overall_score,
        "max_score": max_score,
        "percentage": int(percentage), 
        "recommendation_band": band
    }
    
@tool("load_skill_synonyms_tool")
def load_skill_synonyms_tool(z_input: str = ""): 
    """Loads the skill synonyms mapping to help match resume skills to rubric categories."""
    print("---calling load_skill_synonyms_tool()---\n")
    
    synonyms_path = Path("data/p004_resume_screening_crew_dataset/metadata/skill_synonyms.json")
    try:
        with open(synonyms_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as err:
        return {"error": f"Failed to load synonyms: {err}"}
