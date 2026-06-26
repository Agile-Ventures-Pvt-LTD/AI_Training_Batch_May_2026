from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import pandas as pd

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

jd_path="data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md"


# tool - 1
def read_job_description_tool(jd_path):
    """
    Reads the job description file from the given path.
    
    Parameters:
    jd_path (str): Path to the job description file.
    
    Returns:
    dict: {
        "success": bool,
        "content": str,
        "source_file": str
    }
    """
    # Initialize the response dictionary
    response = {
        "success": False,
        "content": "",
        "source_file": ""
    }
    
    # Check if the file exists
    if os.path.exists(jd_path) and os.path.isfile(jd_path):
        try:
            with open(jd_path, 'r', encoding='utf-8') as file:
                content = file.read()
            response["success"] = True
            response["content"] = content
            response["source_file"] = os.path.basename(jd_path)
        except Exception as e:
            # Handle file reading errors
            response["content"] = f"Error reading file: {str(e)}"
    else:
        response["content"] = "File does not exist."
    
    return response


  


# Function to read a resume file
def read_resume_tool(resume_path: str) -> str:
    """
    Reads the content of a candidate resume from the given file path.
    
    Parameters:
    - resume_path (str): Path to the resume file
    
    Returns:
    - str: The textual content of the resume
    
    Raises:
    - FileNotFoundError: If the file does not exist at the given path
    - ValueError: If the file is empty or unreadable
    """
    if not os.path.exists(resume_path):
        raise FileNotFoundError(f"Resume file not found: {resume_path}")
    
    try:
        with open(resume_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                raise ValueError("Resume file is empty")
            return content
    except Exception as e:
        raise ValueError(f"Error reading resume file: {e}")






# Example Rubric Class
class LoadScreeningRubric:
    """
    Tool for evaluating load screening rubric.
    Criteria and scoring can be customized as needed.
    """
    def __init__(self, rubric_criteria):
        """
        rubric_criteria: Dict of criteria and their score thresholds
        Example:
        {
            'credit_score': 700,
            'income': 50000,
            'loan_history': 2
        }
        """
        self.rubric_criteria = rubric_criteria

    def evaluate(self, load_data):
        """
        load_data: Pandas DataFrame with columns matching rubric_criteria
        Returns DataFrame with evaluation results
        """
        results = []
        for _, row in load_data.iterrows():
            evaluation = {}
            evaluation['id'] = row.get('id', None)
            score = 0
            for criterion, threshold in self.rubric_criteria.items():
                if row.get(criterion, 0) >= threshold:
                    score += 1
            evaluation['passed_criteria'] = score
            evaluation['total_criteria'] = len(self.rubric_criteria)
            evaluation['is_pass'] = score == len(self.rubric_criteria)
            results.append(evaluation)
        return pd.DataFrame(results)
    








def find_resume(candidate_id, search_directory='resumes'):
    """
    Search for a resume file for a given candidate ID in the specified directory.

    Parameters:
    - candidate_id (str): The unique ID of the candidate
    - search_directory (str): Directory where resume files are stored. Defaults to 'resumes'.

    Returns:
    - list: List of matching file paths. Empty list if no file is found.
    """
    matching_files = []
    
    # Traverse the directory
    for root, dirs, files in os.walk(search_directory):
        for file in files:
            # Check if candidate ID is in the filename
            if candidate_id in file:
                # Store full path
                matching_files.append(os.path.join(root, file))
    
    return matching_files




# Function to calculate total score based on weighted criteria
def calculate_score(scores, weights=None):
    """
    Calculate a final score based on given scores and optional weights.
    
    Parameters:
    scores (dict): Dictionary of criterion names and their scores. Example: {'math': 90, 'english': 85}
    weights (dict, optional): Dictionary of criterion names and their respective weights (0 to 1). 
                              The sum should ideally be 1. If None, all criteria are equally weighted.
    
    Returns:
    float: Total weighted score
    """
    if not weights:
        # If no weights provided, assign equal weight to each criterion
        num_criteria = len(scores)
        weights = {key: 1/num_criteria for key in scores}
    
    # Ensure all criteria in scores have corresponding weights
    for key in scores:
        if key not in weights:
            weights[key] = 0  # default weight 0 if not specified
    
    # Calculate weighted score
    total_score = sum(scores[key] * weights[key] for key in scores)
    return total_score



from typing import List, Dict

# Function to calculate skill match
def skill_matcher(job_skills: List[str], candidate_skills: List[str]) -> Dict:
    """
    Compare job description skills and candidate skills.
    
    Args:
        job_skills (List[str]): Skills required for the job.
        candidate_skills (List[str]): Skills listed in the candidate's resume.
    
    Returns:
        Dict: Result containing matched skills, partial matches, missing skills, match percentage.
    """
    # Normalize skills (lowercase and strip whitespaces)
    job_skills_set = set([skill.strip().lower() for skill in job_skills])
    candidate_skills_set = set([skill.strip().lower() for skill in candidate_skills])
    
    # Matched skills
    matched = list(job_skills_set & candidate_skills_set)
    
    # Skills present in candidate but only partially match (optional or fuzzy logic can be added here)
    partial_matches = list(candidate_skills_set - job_skills_set)
    
    # Missing skills - required but not in candidate profile
    missing = list(job_skills_set - candidate_skills_set)
    
    # Simple match percentage
    match_percentage = round((len(matched) / len(job_skills_set)) * 100, 2) if job_skills_set else 0
    
    return {
        "matched_skills": [skill.capitalize() for skill in matched],
        "partial_matches": [skill.capitalize() for skill in partial_matches],
        "missing_skills": [skill.capitalize() for skill in missing],
        "match_percentage": match_percentage
    }





import json




import os
from datetime import datetime

# Function to save the report
def save_report_tool(report_content, report_name="final_report"):
    """
    Saves the final report content to the outputs/ folder.
    
    Args:
        report_content (str): Content of the report to save.
        report_name (str): Optional base name for the report file.
        
    Returns:
        str: Path to the saved report file.
    """
    # Ensure outputs directory exists
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{report_name}_{timestamp}.txt"
    file_path = os.path.join(output_dir, filename)

    # Save the report content to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    return file_path




import json

# Define required fields
REQUIRED_FIELDS = ["candidate_id", "candidate_name", "role_title","overall_score","max_score","percentage","recommendation","executive_summary","strengths","gaps","interview_focus_areas","interview_question","evidence","human_review_note"]


def validate_report(report):
    """
    Validates that all required fields are present in the report.
    
    Args:
        report (dict): The report data as a dictionary.
    
    Returns:
        dict: Validation result with missing fields if any.
    """
    missing_fields = [field for field in REQUIRED_FIELDS if field not in report]
    if missing_fields:
        return {"valid": False, "missing_fields": missing_fields}
    return {"valid": True, "missing_fields": []}

