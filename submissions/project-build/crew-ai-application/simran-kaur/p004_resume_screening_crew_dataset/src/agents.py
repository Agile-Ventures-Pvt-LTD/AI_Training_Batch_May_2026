from config import groq_api_key, dataset_path, output_path, groq_model
from crewai import Agent
from tools import read_job_description,read_resume_tool,candidate_index_lookup,load_screening_rubric,score_calculator,save_report,skill_matcher_tool
from crewai import LLM
from dotenv import load_dotenv
load_dotenv()
import os

job_description_file = dataset_path/job_description/jd_ai_engineer.md

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")


# using LLM class from crewai

llm = LLM(
    model=os.getenv("GROQ_MODEL", "groq/llama-3.1-8b-instant"),
    api_key=groq_api_key,
    max_tokens=700,
    temperature=0.3,
    tool_choice="auto",
    )


# =============================1.Job description analyst agent============================

job_description_analyst = Agent(
    role='Job Description Analyst Agent',
    goal= """ Understand the job description from the given user input  and extract the relevant data from {job_description_file} and provide provide the answer in sctructured json format Expected output structure:'
    {
    "role_title": "",
    "required_skills": [],
    "preferred_skills": [],
    "responsibilities": [],
    "experience_expectation": "",
    "evaluation_criteria": []
     } """,
    verbose=False,
    memory=False,
    backstory=(
       "Expert in understanding the user job description based on the user input"
       "finding relevant match from the jd_ai_engineer.md file given in the project."
       "get all JD requirements (job description requirements) for the job description"
       "provide result in structured JSON."
    ),
    tools=[read_job_description],
    allow_delegation=False,
    max_iter=2,
    llm=llm
)

# ===============================2. Resume Extraction Agent===============================

resume_extraction_agent = Agent(
    role='Resume Extraction Expert',
    goal=""" The goal is to take candidate resume file as input and  Extract structured candidate information from the resume.Expected output structure:
    {
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
    """,
    verbose=False,
    memory=False,
    backstory=(
        "look up the candidate details from the provided candidate resume file"
        "extractiong all the relevant information mentioned in the candidate profile"
        "provide the result in structured JSON"
    ),
    tools=[candidate_index_lookup,read_resume_tool]
    allow_delegation=False,
    max_iter=2,
    llm=llm


)


# ===========================3.Skill and Experience Matching Agent==========================

skill_and_experience_matching_agent = Agent(
    role='Skill and Experience Matching Expert',
    goal=""" The goal is to Compare JD requirements provided by {job_description_analyst} with the candidate profile provided by {resume_extraction_agent}.
    Expected output structure:
    {
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
    "recommendation_band": ""
    }
    """,
    verbose=False,
    memory=False,
    backstory=(
        "make use of screening_rubic.json to get the matching score."
        "See all skill related sysnonyms from skill_synonyms.json to analyse accurately"
        "make proper comparison between jd_analysis.json and resume_profile.json "
        "provide the result in structured JSON"
    ),
    allow_delegation=False,
    max_iter=2,
    llm=llm


)

#===================================4. Interview Planning Agent=============================

interview_planning_agent = Agent(
    role=' Interview Planning Expert',
    goal=""" The goal is to  Generate candidate-specific interview questions based on the results of {jd_analysis.json}, {resume_profile.json}, {match_score.json} provided by the 3 agents job_description_analyst,resume_extraction_agent and skill_and_experience_matching_agent.

    Minimum required questions:
    3 technical questions
    2 project deep-dive questions
    2 scenario questions
    2 gap-validation questions

    Expected output structure of the agent:
    {
        "interview_focus_areas": [],
        "technical_questions": [],
        "project_deep_dive_questions": [],
        "scenario_questions": [],
        "gap_validation_questions": []
    }
    """,
    verbose=False,
    memory=False,
    backstory=(
        "Based on the matching of job description and the candidate resume ,prepare relevant interview questions"
        "Cover all minimum required questions"
        "provide most relevant questions for job interview preparation"
    ),
    allow_delegation=False,
    max_iter=2,
    llm=llm


)

# ===============================5. Final Recommendation Agent===============================

recommendation_agent = Agent(
    role='Interview Screening Expert',
    goal="""The goal is to generate the final screening report based on the result generated by all the other 4 agents  {job_description_analyst},{resume_extraction_agent},{skill_and_experience_matching_agent} and {interview_planning_agent}.
    Expected output structure:
    {
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
        "human_review_note": ""
    }
    """,

    verbose=False,
    memory=False,
    backstory=(
        "find the potential candidate as per the job decsription"
        "provide recommendation as STRONG_MATCH | MODERATE_MATCH | WEAK_MATCH | NEEDS_MANUAL_REVIEW based on screening and analysing other 4 agents result"
        "generate a complete final screening report in structured JSON"        
    ),
    allow_delegation=False,
    max_iter=2,
    llm=llm


)

