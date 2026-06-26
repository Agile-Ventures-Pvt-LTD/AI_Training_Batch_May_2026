from crewai.tools import tool
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import JSONLoader
import json
import markdown



@tool
def read_job_description_tool(jd_path)->dict:
        """This tool is used to read the job discription """
        try:
            with open(jd_path, "r", encoding="utf-8") as file:
                docs = file.read()
            
            return {
                "success": "true",
                "content": docs,
                "source_file": "jd_ai_engineer.md"
                }   
        except Exception as e:
            print(f"Can not load document: {e}")
            return None


@tool
def read_resume_tool(resume_path)->dict:
        """This tool is use to read resume of candidate"""
        try:
            with open(resume_path, "r", encoding="utf-8") as file:
                docs = file.read()
            return {
                "success": "true",
                "content":docs,
                }   
        except Exception as e:
            print(f"Can not load document: {e}")
            return None 
        


@tool
def candidate_index_lookup_tool(id:str)->dict:
    """This tool is used to look for candidate."""
    try:
        if id=='CAND-001':
              return{
                   "found": True,
                    "candidate_id": "CAND-001",
                    "candidate_name": "Rohan Mehta",
                    "resume_file": "candidate_001_rohan_mehta.md"
              }
        elif id=='CAND-002':
              return{
                   "found": True,
                    "candidate_id": "CAND-002",
                    "candidate_name": "Priya Sharma",
                    "resume_file": "candidate_002_priya_sharma.md"
              }
        elif id=='CAND-003':
              return{
                   "found": True,
                    "candidate_id": "CAND-003",
                    "candidate_name": "Neha Gupta",
                    "resume_file": "candidate_002_neha_gupta.md"
              }
        elif id=='CAND-004':
              return{
                   "found": True,
                    "candidate_id": "CAND-004",
                    "candidate_name": "Arjun Nair",
                    "resume_file": "candidate_002_arjun_nair.md"
              }
        elif id=='CAND-005':
              return{
                   "found": True,
                    "candidate_id": "CAND-005",
                    "candidate_name": "Sara Khan",
                    "resume_file": "candidate_002_sara_khan.md"
              }
        else:
            return{
                "found": False,
                "message": "Candidate ID not found."
            }
    except Exception as e:
        print(f"Can not find data: {e}")
        return None 
         

@tool
def load_screening_rubric_tool(rubic_path):
    """This tool is used to load rubric for screening"""
    try:
        with open(rubic_path, 'r', encoding='utf-8') as file:
            json_string = file.read()
        try:
            json_data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        return json_data
    except Exception as e:
        print(f"Can not find data: {e}")
        return None
    

 
@tool
def score_calculator_tool(category_scores: dict) -> dict:
    """Calculates total score, percentage, and recommendation band for a candidate."""
    overall_score = sum(category_scores.values())
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
       
    return {
        "overall_score": overall_score,
        "max_score": max_score,
        "percentage": int(percentage) if percentage.is_integer() else round(percentage, 1),
        "recommendation_band": band
    }
            
     



@tool
def save_report_tool(data):
     """This tool is used to save final report""" 
     output_dir = Path("outputs")
     output_dir.mkdir(exist_ok=True)

     output_file = output_dir / "CAND-001_screening_report.json"

     with open(output_file, "w") as f:
        json.dump(data, f, indent=4)


     


 