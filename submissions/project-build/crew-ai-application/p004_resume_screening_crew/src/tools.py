import os
import json
import csv
from crewai.tools import tool
from crewai.tools import tool

def _get_dataset_path() -> str:
    return os.getenv("DATASET_PATH", "data/p004_resume_screening_crew_dataset")

def _get_output_path() -> str:
    return os.getenv("OUTPUT_PATH", "outputs")


@tool("read_job_description_tool")
def read_job_description(jd_path:str) -> dict:
    """Reads the job description md file from the given path."""
    try:
        if not os.path.exists(jd_path):
            return {"success": False, "error": f"File not found: {jd_path}"}
            
        with open(jd_path, "r", encoding="utf-8") as f:
            jd_content = f.read()
            
        return {
            "success": True,
            "content": jd_content,
            "source_file": os.path.basename(jd_path)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    


@tool("read_resume_tool")
def read_resume(resume_path: str) -> dict:
    """Reads a candidate resume md file from the given path."""
    try:
        if not os.path.exists(resume_path):
            return {"success": False, "error": f"File not found: {resume_path}"}
            
        with open(resume_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        return {
            "success": True,
            "content": content,
            "source_file": os.path.basename(resume_path)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    

@tool("candidate_index_lookup_tool")
def candidate_index_lookup(candidate_id: str) -> dict:
    """Finds the basic details and correct resume file name for a given candidate ID."""
    try:
        csv_path = os.path.join(_get_dataset_path(), "metadata", "candidate_index.csv")
        if not os.path.exists(csv_path):
            return {"found": False, "message": "Candidate index file does not exist."}           
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("candidate_id") == candidate_id:
                    return {
                        "found": True,
                        "candidate_id": row.get("candidate_id"),
                        "candidate_name": row.get("candidate_name"),
                        "resume_file": row.get("resume_file")
                    }
        return {"found": False, "message": "Candidate ID not found."}
    except Exception as e:
        return {"found": False, "message": str(e)}
    

@tool("load_screening_rubric_tool")
def load_screening_rubric() -> dict:
    """Loads the fixed scoring rubric configuration containing the 8 evaluation categories."""
    try:
        json_path = os.path.join(_get_dataset_path(), "metadata", "screening_rubric.json")
        if not os.path.exists(json_path):   
            return {"found": False, "message": "Screening rubric file does not exist."}       
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}
    
@tool("score_calculator_tool")
def score_calculator(category_scores: dict) -> dict:
    """Calculate total score, percentage, and maps it to the correct recommendation band."""
    try:
        overall_score = sum(category_scores.values())
        max_score = 40
        percentage = int((overall_score / max_score) * 100)
        
        if percentage >= 80:
            recommendation_band = "STRONG_MATCH"
        elif percentage >= 60:
            recommendation_band = "MODERATE_MATCH"
        elif percentage >= 40:
            recommendation_band = "WEAK_MATCH"
        else:
            recommendation_band = "NEEDS_MANUAL_REVIEW"
            
        return {
            "overall_score": overall_score,
            "max_score": max_score,
            "percentage": percentage,
            "recommendation_band": recommendation_band
        }
    except Exception as e:
        return {"error": str(e)}


@tool("save_report_tool")
def save_report(candidate_id: str, report_data: dict) -> dict:
    """Save the final candidate screening json report to the outputs folder."""
    try:
        output_dir = _get_output_path()
        os.makedirs(output_dir, exist_ok=True)
        
        file_name = f"{candidate_id}_screening_report.json"
        file_path = os.path.join(output_dir, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4)
            
        return {"success": True, "saved_path": file_path}
    except Exception as e:
        return {"success": False, "error": str(e)}

