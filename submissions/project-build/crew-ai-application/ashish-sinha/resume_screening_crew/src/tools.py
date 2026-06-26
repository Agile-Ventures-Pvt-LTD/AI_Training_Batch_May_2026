import os
import json
import csv
import pandas as pd
from typing import Dict,Any,List
from crewai.tools import tool
from pydantic import BaseModel,Field
from scoring import ScoringEngine

@tool("Read Job Description Tool")
def read_job_description_tool(jd_path:str) -> Dict[str,Any]:
    """
    Read the Job descriptions from the markdown file from the given path.
    """
    try:
        with open(jd_path,"r",encoding='utf-8') as f:
            content = f.read()
        return {"sucess":True,"content":content,"source_file":os.path.basename(jd_path)}
    except Exception as e:
        return{"sucess":False,"error":str(e)}
    
@tool("Read Resume Tool")
def read_resume_tool(resume_path:str) -> Dict[str,Any]:
    """
    Read the candidate's Resume markdown file from the given path. 
    """
    try:
        with open(resume_path,"r",encoding='utf-8') as f:
            content = f.read()
        return {"sucess":True,"content":content,"source_file":os.path.basename(resume_path)}
    except Exception as e:
        return{"sucess":False,"error":str(e)}
    
@tool("Candidate Index Lookup Tool")
def candidate_index_lookup_tool(candidate_id: str) -> Dict[str, Any]:
    """
    Finds the resume file name and basic data for a specific candidate ID.
    """
    csv_path: str = "data/p004_resume_screening_crew_dataset/metadata/candidate_index.csv"
    if not os.path.exists(csv_path):
        return {"found": False, "message": f"CSV file not found at this path {csv_path}."}
    
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    match = df[df['candidate_id'].str.strip() == candidate_id.strip()]
    
    if match.empty:
        return {"found": False, "message": "Candidate ID not found."}
    
    row = match.iloc[0]
    return {
        "found": True,
        "candidate_id": str(row['candidate_id']),
        "candidate_name": str(row['candidate_name']),
        "resume_file": str(row['resume_file'])
    }

@tool("Load Screening Rubric Tool")
def load_screening_rubric_tool(rubric_path: str = "data/p004_resume_screening_crew_dataset/metadata/screening_rubric.json") -> Dict[str, Any]:
    """Loads the approved category scoring rubric criteria."""
    try:
        with open(rubric_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        return {
            "categories": ["python_programming", "sql_database_skills", "api_integration", "llm_application_development", "agent_frameworks", "rag_understanding", "testing_and_quality", "communication"],
            "score_range": "0 to 5",
            "max_score": 40
        }

@tool("Score Calculator Tool")
def score_calculator_tool(category_scores: Dict[str, int]) -> Dict[str, Any]:
    """Calculates overall score, matching percentage, and target recommendation band using the engine."""
    return ScoringEngine.calculate_metrics(category_scores)

# @tool("Score Calcuator Tool")
# def score_calculator_tool(category_scores:Dict[str,int]) -> Dict[str,Any]:
#     """
#     Calcuate Total Scor, matching percentage, and recommendation band.
#     """
#     overall_score = sum(category_scores.values())
#     max_score = 40
#     percentage = (overall_score/max_score)*100

#     if percentage >= 80:
#         band="STRONG_MATCH"
#     elif percentage >= 60:
#         band="M0DERATE_MATCH"
#     elif percentage >= 40:
#         band= "WEAK_MATCH"
#     else:
#         band= "NEED_MANUAL_REVIEW"
    
#     return {
#         "overall_score": overall_score,
#         "max_score": max_score,
#         "percentage": round(percentage, 2),
#         "recommendation_band": band
#     }

@tool("Save Report Tool")
def save_report_tool(candidate_id: str, report_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Saves the final candidate structural JSON report into the output directory.
    """
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{candidate_id}_screening_report.json"
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        return {"success": True, "saved_path": filepath}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
@tool("Validate Report Schema Tool")
def validate_report_schema_tool(report_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates that all mandatory fields are present inside the output schema.
    """
    required_fields = [
        "candidate_id", "candidate_name", "role_title", "overall_score", 
        "max_score", "percentage", "recommendation", "executive_summary", 
        "strengths", "gaps", "interview_focus_areas", "interview_questions", 
        "evidence", "human_review_note"
    ]
    missing_fields = [field for field in required_fields if field not in report_data]
    return {
        "schema_valid": len(missing_fields) == 0,
        "missing_fields": missing_fields
    }