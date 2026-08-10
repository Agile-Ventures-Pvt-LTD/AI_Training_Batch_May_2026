from crewai.tools import tool
from pathlib import Path
from dotenv import load_dotenv
from config import dataset_path
import json
import pandas
load_dotenv()
import os

# jd_path = "..data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md"




# Get current working directory
current_dir = os.getcwd()
print("Current Directory:", current_dir)

# Get parent directory
parent_dir = os.path.dirname(current_dir)
print("Parent Directory:", parent_dir)

jd_path = f"{parent_dir}/data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md"


# ,encoding="utf-8"      encoding (str): File encoding (default: 'utf-8').  encoding=encoding

#=============================TOOL1------------------------------------

@tool("read_job_description_tool")
def read_job_description(jd_path):
   
    """
    Reads the content of  job description Markdown (.md) file.

    Parameters:
        jd_path (str): Path to the Markdown file.
       

    Returns:
        dictionary with keys as "success", "content" ,"source_file"

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not '.md'.
        IOError: If there is an error reading the file.
    """


    jd_path = "..data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md"

    if not os.path.exists(jd_path):
        raise FileNotFoundError(f"File not found: {jd_path}")


    if not jd_path.lower().endswith(".md"):
        raise ValueError("The file must have a '.md' extension.")

    try:
        with open(jd_path, "r", encoding="utf-8") as file:

            return {
                "success": True,
                "content": file.read(),
                "source_file": "jd_ai_engineer.md"
                }
        
    except Exception as e:
        raise IOError(f"Error reading file '{jd_path}': {e}")




#==================================TOOL2======================================

@tool(" read_resume_tool")
def read_resume(resume_path):
   
    """
    Takes path as input such as resume_path="data/p004_resume_screening_crew_dataset/resumes/candidate_001_rohan_mehta.md" based on the user query.

    It takes user input, from there it takes candidate name and find candidate resume .md file from  resume_path="..data/p004_resume_screening_crew_dataset/resumes/

    Reads the content of  job description Markdown (.md) file.

    Parameters:
        jd_path (str): Path to the Markdown file.
       

    Returns:
        dictionary with keys as "success", "content" ,"source_file"

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not '.md'.
        IOError: If there is an error reading the file.
    """
    # Validate file existence
    if not os.path.exists(resume_path):
        raise FileNotFoundError(f"File not found: {resume_path}")

    # Validate file extension
    if not jd_path.lower().endswith(".md"):
        raise ValueError("The file must have a '.md' extension.")

    try:
        with open(resume_path, "r", encoding="utf-8") as file:

            return {
                "success": True,
                "content": file.read(),
                "source_file": resume_path
                }
        
    except Exception as e:
        return {
            "success": False,
            "content": e
        }
        # raise IOError(f"Error reading file '{resume_path}': {e}")


#==========================TOOL3 ==================================

@tool(" candidate_index_lookup_tool")
def candidate_index_lookup(candidate_id):
   
    """
    The tool purpose is to Finds the resume file for a candidate ID in candidate_index.csv
    It take input as:
    Input:
    {
    "candidate_id": "CAND-001"
    }

    It takes user input, from there it takes candidate_id and find candidate resume .md file from  resume_path="..data/p004_resume_screening_crew_dataset/resumes/
    If the candidate_id is CAND-001, then take 001 and search for resume files starting from candidate_001

    Reads the content of  job description Markdown (.md) file.

    Parameters:
        jd_path (str): Path to the Markdown file.
       

    Returns:
        return dictionary with keys as follows
        "found": true if file found,
        "candidate_id" : "CAND-001",
        "candidate_name": name of the candidate such as "Rohan Mehta",
        "resume_file":  name of the resume file such as "candidate_001_rohan_mehta.md"

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not '.md'.
        IOError: If there is an error reading the file.
    """
    file_path = Path(__file__).parent.parent /"data/p004_resume_screening_crew_dataset"/"metadata"/"candidate_index.csv"

    try:
        # Check if file exists
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' not found.")
            return None
        
        # Read CSV file
        df = pd.read_csv(file_path, delimiter=delimiter)
        print(f"Successfully loaded '{file_path}' with {len(df)} rows and {len(df.columns)} columns.")
        return {
            "found": True,
            "candidate_id": df[candidate_id],
            "candidate_name": df[candidate_name],
            "resume_file": df[resume_file]
            }
    
   



#-------------------------TOOL 4===============================

@tool("  load_screening_rubric_tool")
def load_screening_rubric():
   
    """
    Purpose: Loads the scoring rubric from: metadata/screening_rubric.json

    Parameters:
      
       

    Returns:
        return dictionary with keys as follows
        Output:
        {
        "categories": [
        "python_programming",
        "sql_database_skills",
        "api_integration",
        "llm_application_development",
        "agent_frameworks",
        "rag_understanding",
        "testing_and_quality",
        "communication"
        ],
        "score_range": "0 to 5",
        "max_score":40

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not '.md'.
        IOError: If there is an error reading the file.
    """

 
    DATA_FILE = Path(__file__).parent.parent /"data/p004_resume_screening_crew_dataset"/"metadata"/"candidate_index.csv"
    
    with open(DATA_FILE, "r") as f: 
        return json.load(f) 
    
     


#===========================TOOL 5===================================

@tool("score_calculator_tool")
def score_calculator(category_scores:dict):
   
    """
    Purpose:Calculates total score, percentage, and recommendation band.
    Expected calculation:
    overall_score = sum(category_scores)
    max_score = 40
    percentage = overall_score / 40 * 100
    Recommendation bands:
    Percentage Recommendation
    80–100 STRONG_MATCH
    60–79 MODERATE_MATCH
    Percentage Recommendation
    40–59 WEAK_MATCH
    Below 40 NEEDS_MANUAL_REVIEW

    Parameters:
            {
        "category_scores": {
        "python_programming": 4,
        "sql_database_skills": 3,
        "api_integration": 4,
        "llm_application_development": 4,
        "agent_frameworks": 3,
        "rag_understanding": 3,
        "testing_and_quality": 3,
        "communication": 4
        }
        }
       

    Returns:
        return dictionary with keys as follows
        Output:
        Output:
        {
            "overall_score": 28,
            "max_score": 40,
            "percentage": 70,
            "recommendation_band": "MODERATE_MATCH"
        }
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not '.md'.
        IOError: If there is an error reading the file.
    """

    overall_score = sum(category_scores)
    max_score = 40
    percentage = overall_score / 40 * 100

    if percentage>=80 and percentage<=100:
        recommendation_band="STRONG_MATCH"
    elif percentage>=60 and percentage<=79:
        recommendation_band="MODERATE_MATCH"
    elif percentage>=40 and percentage<=59:
        recommendation_band="WEAK_MATCH"
    else
        recommendation_band="NEEDS_MANUAL_REVIEW"

    return {
"overall_score":overall_score,
"max_score": max_score,
"percentage": percentage,
"recommendation_band": recommendation_band
    }

#==============================TOOL 6==================================

@tool(" save_report_tool")
def  save_report():
   
    """
    Purpose:
    Saves the final report to the outputs/ folder.
    Required output:
    outputs/CAND-001_screening_report.json
    Optional output:
    outputs/CAND-001_screening_report.md
    """


@tool
def skill_matcher_tool():
    """
    Compares job skills with candidate resume skills.
    Output:
    {
    "matched_skills": [],
    "partial_matches": [],
    "missing_skills": [],
    "match_percentage": 0
    }"""
    
