import os
import json
import csv
from crewai.tools import tool
from config import DATASET_PATH
from scoring import load_rubric, match_skills, calculate_score
from output_writer import validate_schema, save_report

@tool("read_job_description_tool")
def read_job_description_tool(jd_path: str) -> str:
    """Reads the job description file from the specified path."""
    full_path = os.path.join(DATASET_PATH, jd_path)
    if not os.path.exists(full_path):
        return json.dumps({"success": False, "error": "Job description file not found."})
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return json.dumps({"success": True, "content": content, "source_file": os.path.basename(jd_path)})

@tool("read_resume_tool")
def read_resume_tool(resume_path: str) -> str:
    """Reads a candidate resume file from the specified path."""
    full_path = os.path.join(DATASET_PATH, resume_path)
    if not os.path.exists(full_path):
        return json.dumps({"success": False, "error": "Resume file not found."})
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return json.dumps({"success": True, "content": content, "source_file": os.path.basename(resume_path)})

@tool("candidate_index_lookup_tool")
def candidate_index_lookup_tool(candidate_id: str) -> str:
    """Finds the resume file and metadata for a given candidate ID."""
    index_path = os.path.join(DATASET_PATH, "metadata", "candidate_index.csv")
    if not os.path.exists(index_path):
        return json.dumps({"found": False, "message": "Candidate index file missing."})
    
    with open(index_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['candidate_id'].strip() == candidate_id.strip():
                return json.dumps({
                    "found": True,
                    "candidate_id": row['candidate_id'],
                    "candidate_name": row['candidate_name'],
                    "resume_file": row['resume_file']
                })
    return json.dumps({"found": False, "message": "Candidate ID not found."})

@tool("load_screening_rubric_tool")
def load_screening_rubric_tool(dummy_input: str = "load") -> str:
    """Loads the scoring rubric categories and constraints."""
    try:
        rubric = load_rubric()
        return json.dumps({
            "categories": list(rubric.get("categories", {}).keys()),
            "score_range": "0 to 5",
            "max_score": 40
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool("skill_matcher_tool")
def skill_matcher_tool(jd_skills: str, candidate_skills: str) -> str:
    """Compares JD skills with candidate resume skills using synonym mapping."""
    result = match_skills(jd_skills, candidate_skills)
    return json.dumps(result)

@tool("score_calculator_tool")
def score_calculator_tool(category_scores_json: str) -> str:
    """Calculates total score, percentage, and recommendation band."""
    try:
        scores = json.loads(category_scores_json) if isinstance(category_scores_json, str) else category_scores_json
        result = calculate_score(scores)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"Invalid score format: {str(e)}"})

@tool("validate_report_schema_tool")
def validate_report_schema_tool(report_json: str) -> str:
    """Validates that the final report contains all required fields."""
    result = validate_schema(report_json)
    return json.dumps(result)

@tool("save_report_tool")
def save_report_tool(candidate_id: str, report_json: str) -> str:
    """Saves the final JSON report to the outputs directory."""
    result = save_report(candidate_id, report_json)
    return json.dumps(result)