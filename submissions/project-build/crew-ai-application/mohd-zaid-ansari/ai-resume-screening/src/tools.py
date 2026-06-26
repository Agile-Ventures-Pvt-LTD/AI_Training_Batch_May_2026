import os
import csv
import json
from crewai.tools import tool

# ===========================================================================================================================
@tool("Read Job Description Tool") 
def read_job_description(jd_path: str) -> dict:
    """Reads and returns the text content of a specified job description file.
    
    Args:
        jd_path (str): The relative or absolute path to the job description file.
                       Example: 'data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md'
    """
    clean_path = jd_path.strip()
    source_file = os.path.basename(clean_path)
    
    if not os.path.exists(clean_path):
        return {
            "success": False,
            "content": f"Error: The file at path '{clean_path}' does not exist.",
            "source_file": source_file
        }
        
    try:
        with open(clean_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        return {
            "success": True,
            "content": content,
            "source_file": source_file
        }
        
    except Exception as e:
        return {
            "success": False,
            "content": f"Error reading file: {str(e)}",
            "source_file": source_file
        }

# ===========================================================================================================================
@tool("Read Resume Tool") 
def read_resume_tool(resume_path: str) -> dict:
    """Reads and returns the text content of a specified candidate resume file."""
    clean_path = resume_path.strip()
    source_file = os.path.basename(clean_path)
    
    if not os.path.exists(clean_path):
        return {
            "success": False,
            "content": f"Error: The file at path '{clean_path}' does not exist.",
            "source_file": source_file
        }
        
    try:
        with open(clean_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        return {
            "success": True,
            "content": content,
            "source_file": source_file
        }
        
    except Exception as e:
        return {
            "success": False,
            "content": f"Error reading file: {str(e)}",
            "source_file": source_file
        }
    
# =============================================================================================================================
@tool("Candidate Index Lookup Tool")
def candidate_index_lookup_tool(candidate_id: str) -> dict:
    """Looks up a candidate ID in the index CSV file to return their resume file name."""
    csv_path = "data/p004_resume_screening_crew_dataset/metadata/candidate_index.csv"
    clean_id = candidate_id.strip().upper()
    
    if not os.path.exists(csv_path):
        return {
            "found": False,
            "message": f"Error: Metadata file not found at '{csv_path}'"
        }
        
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                if row.get("candidate_id", "").strip().upper() == clean_id:
                    return {
                        "found": True,
                        "candidate_id": clean_id,
                        "candidate_name": row.get("candidate_name", "").strip(),
                        "resume_file": row.get("resume_file", "").strip()
                    }
        return {
            "found": False,
            "message": "Candidate ID not found."
        }
        
    except Exception as e:
        return {
            "found": False,
            "message": f"Error reading index data: {str(e)}"
        }

# ==============================================================================================================================
@tool("Load Screening Rubric Tool")
def load_screening_rubric_tool() -> dict:
    """Loads and returns the structured scoring rubric from the metadata JSON file."""
    path = "data/p004_resume_screening_crew_dataset/metadata/screening_rubric.json"
    
    if not os.path.exists(path):
        other_path = "metadata/screening_rubric.json"
        if os.path.exists(other_path):
            path = other_path
        else:
            return {
                "error": f"Error: Rubric file not found at '{path}'"
            }
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        return {
            "error": f"Error reading rubric data: {str(e)}"
        }

# ============================================================================================================================
@tool("Score Calculator Tool")
def score_calculator_tool(category_scores: dict) -> dict:
    """Calculates overall score, percentage, and the matching recommendation band."""
    try:
        overall_score = sum(int(score) for score in category_scores.values())
        max_score = 40
        percentage = (overall_score / max_score) * 100
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
            "percentage": round(percentage, 2) if percentage % 1 != 0 else int(percentage),
            "recommendation_band": recommendation_band
        }
        
    except Exception as e:
        return {
            "error": f"Failed to calculate scores: {str(e)}"
        }

# =============================================================================================================================
@tool("Save Report Tool")
def save_report_tool(candidate_id: str, report_data: dict, markdown_content: str = "") -> dict:
    """Saves the candidate screening report to the outputs/ directory in JSON and optional Markdown format."""
    id = candidate_id.strip().upper()
    output_dir = "outputs"
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        json_file_name = f"{id}_screening_report.json"
        json_path = os.path.join(output_dir, json_file_name)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4)
            
        md_file_name = f"{id}_screening_report.md"
        md_path = os.path.join(output_dir, md_file_name)
        if markdown_content.strip():
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
        return {
            "success": True,
            "message": f"Reports successfully saved to {output_dir}/",
            "json_path": json_path,
            "md_path": md_path if markdown_content.strip() else None
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to save report: {str(e)}"
        }
