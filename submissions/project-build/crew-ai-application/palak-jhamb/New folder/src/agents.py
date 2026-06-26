from tools import read_job_description_tool,read_resume_tool,load_screening_rubric_tool,candidate_index_lookup_tool
from crewai import Agent
from config import llm


#this is an agent tha analyzes job discription
job_review = Agent(
  role='Senior HR',
  goal='Analyze the job discription and understand the requirements to check for candidate.',
  backstory=(
    "You are a senior HR in the company , you are looking for a candidate with the provided job discription." \
    "your current resp0onsiblity is to  Understand the job description"
    "you have a tool to read the job discription, use that to get job discription"
    "return output in json format "
    "expected output format is provided below"
    """output:  {
        "role_title": "",
        "required_skills": [],
        "preferred_skills": [],
        "responsibilities": [],
        "experience_expectation": "",
        "evaluation_criteria": []"
        }
        """
  ),
  verbose=True, 
  allow_delegation=False, 
  tools=[read_job_description_tool], 
  llm=llm,
  memory=True 
)



#this is an agent tha analyzes candidate
resume_extraction = Agent(
  role='Senior Talent Acquisition specialist',
  goal='Analyze the resume and find out if candidate is worth for ai role according to requirements.',
  backstory=(
    "You are a senior HR in the company , you are looking for a candidate with the provided job discription." \
    "your current responsiblity is to gather information about candidate"
    "You have a tool candidate_index_lookup_tool, using which you can find out the resume file path "
    "you have a tool to read the resume of candidate, use that to get resume details using tool read_resume_tool"
    "return output in json format "
    "expected output format is provided below"
    """output:  {
        "candidate_id": "",
        "candidate_name": "",
        "current_role": "",
        "years_experience": "",
        "skills": [],
        "projects": [],
        "experience_summary": [],
        "education": [],
        "certifications": []
        }
        """
  ),
  verbose=True, 
  allow_delegation=False, 
  tools=[read_resume_tool,candidate_index_lookup_tool], 
  llm=llm,
  memory=True 
)


Skill_and_Experience_Matching_Agent=Agent(
  role='Senior skill and experience matchng specialist',
  goal='Analyze the resume and find out if candidate is worth for ai role according to requirements.',
  backstory=(
    "You are a senior specialist in company. you have to evaluate a candidate based on input provided" \
    "your current responsiblity is to find out weather candidate is a good fit for the role or not"
    "you have a tool to get the rubric for evaluation . use that to find out criteria"
    "return output in json format "
    "expected output format is provided below"
    """output:  {
        "matched_skills": [],
        "partial_matches": [],
        "missing_skills": [],
        "category_scores": {
            "python_programming": 0,
            "sql_database_skills": 0,
            "api_integration": 0,
            "llm_application_development": 0,
            "agent_frameworks": 0,
            "rag_understanding": 0,
            "testing_and_quality": 0,
            "communication": 0
        },
        "overall_score": 0,
        "max_score": 40,
        "percentage": 0,
        "recommendation_band": "
        }
        """
  ),
  verbose=True, 
  allow_delegation=False, 
  tools=[load_screening_rubric_tool], 
  llm=llm,
  memory=True 
)



Interview_Planning_Agent = Agent(
  role='Senior Interview Planner',
  goal="Generate the interview plan",
  backstory=(
    "You are a senior interviewer in a company. generate a plan for interview based on data provided regarding jd, candidate and rubric."
    "Minimum required questions:"
       " 3 technical questions"
        "2 project deep-dive questions"
        "2 scenario questions"
        "2 gap-validation questions"
    "return output in json format "
    "expected output format is provided below"
    """output:  {
        interview_focus_areas": [],
        "technical_questions": [],
        "project_deep_dive_questions": [],
        "scenario_questions": [],
        "gap_validation_questions": []
        """
  ),
  verbose=True, 
  allow_delegation=False, 
  tools=[], 
  llm=llm,
  memory=True 

)

Final_Recommendation_Agent=Agent(
  role='Senior Decision maker',
  goal="Produce the final screening report",
  backstory=(
    "You are a senior interviewer in a company. your task is to make final recommendation" 
    "based on all available context generate the final report"      
    "return output in json format "
    "expected output format is provided below"
    """output:  {
        "candidate_id": "",
        "candidate_name": "",
        "role_title": "",
        "overall_score": 0,
        "max_score": 40,
        "percentage": 0,
        "recommendation": "STRONG_MATCH | MODERATE_MATCH | WEAK_MATCH | 
        NEEDS_MANUAL_REVIEW",
        "executive_summary": "",
        "strengths": [],
        "gaps": [],
        "interview_focus_areas": [],
        "interview_questions": {
        "technical_questions": [],
        "project_deep_dive_questions": [],
        "scenario_questions": [],
        "gap_validation_questions": []
        },
        "evidence": [],
        "human_review_note": "
        }
        """
  ),
  verbose=True, 
  allow_delegation=False, 
  tools=[], 
  llm=llm,
  memory=True 
)
