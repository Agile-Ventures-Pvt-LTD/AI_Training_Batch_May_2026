from crewai import LLM, Agent, Task, Crew, Process
from config import llm
from tools import resume_tools

## Job Description Analyst Agent
job_decription_analyst=Agent(
    role='Job Description Analyst',
    goal="""Understand the job description and give output in the following format:
    {"role_title": "",
"required_skills": [],
"preferred_skills": [],
"responsibilities": [],
"experience_expectation": "",
"evaluation_criteria": []}""",
    verbose=True,
    memory=True,
    backstory=(
       "Expert in understanding Job descriptions and provide relevant summary and information about the job" 
    ),
    tools=[resume_tools],
    allow_delegation=True,
    llm=llm
)

# Resume Extraction Agent
resume_extraction=Agent(
    role='Resume Extraction Agent',
    goal=""" Extract structured candidate information from the resume
    Inputs: candidate resume file

    Expected output file/object:resume_profile.json
Expected output structure:
{
"candidate_id": "",
"candidate_name": "",
"current_role": "",
"years_experience": "",
"skills": [],
"projects": [],
"experience_summary": [],
"education": [],
"certifications": []}""",
    verbose=True,
    memory=True,
    backstory=(
       "Expert in extracting information of the candidate from the resume so that it can be evaluated further" 
    ),
    tools=[resume_tools],
    allow_delegation=True,
    llm=llm
)

#  Skill and Experience Matching Agent
skill_and_experience_matching=Agent(
    role='Skill and Experience Matching Agent',
    goal="""Compare JD requirements with the candidate profile.
Inputs:
jd_analysis.json
resume_profile.json
screening_rubric.json
skill_synonyms.json

Expected output file/object:
match_score.json
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
"recommendation_band": ""}""",
    verbose=True,
    memory=True,
    backstory=(
       "Expert in comparing the Job Description requirements with the candidate profiel and matches according the jobs" 
    ),
    tools=[resume_tools],
    allow_delegation=True,
    llm=llm
)

# Interview Planning Agent
interview_planning_agent=Agent(
    role='Interview Planning Agent',
    goal="""Generate candidate-specific interview questions.
Inputs:
jd_analysis.json
resume_profile.json
match_score.json
Expected output file/object: interview_plan.json

Expected output structure:
{
"interview_focus_areas": [],
"technical_questions": [],
"project_deep_dive_questions": [],
"scenario_questions": [],
"gap_validation_questions": []}""",
    verbose=True,
    memory=True,
    backstory=(
       "Expert in generating the specific questions for interview according to the candidate" 
    ),
    tools=[resume_tools],
    allow_delegation=True,
    llm=llm
)

# Final Recommendation Agent
final_recommendation=Agent(
    role=' Final Recommendation Agent',
    goal="""
 Produce the final screening report.
Inputs:
jd_analysis.json
resume_profile.json
match_score.json
interview_plan.json

Expected output file/object:
candidate_screening_report.json
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
"human_review_note": ""}
""",
    verbose=True,
    memory=True,
    backstory=(
       "Expert in producing final screening report of the candidate based on the relevant job description." 
    ),
    tools=[resume_tools],
    allow_delegation=True,
    llm=llm
)


# Gap Analysis Agent
gap_analysis=Agent(
    role=' Gap Analysis Agent',
    goal="""
Identify missing or weak areas separately.
Expected output:
{
"critical_gaps": [],
"moderate_gaps": [],
"areas_to_probe": []}""",
    verbose=True,
    memory=True,
    backstory=(
       "Expert in analysing the gaps of the candidate" 
    ),
    tools=[resume_tools],
    allow_delegation=True,
    llm=llm
)


# Report Review Agent
report_review=Agent(
    role=' Report Review Agent',
    goal="""Review final report for completeness, schema consistency, and 
evidence quality.
Expected output:
{
"report_complete": true,
"missing_sections": [],
"schema_valid": true,
"review_notes": []}""",
    verbose=True,
    memory=True,
    backstory=(
       "" 
    ),
    tools=[resume_tools],
    allow_delegation=True,
    llm=llm
)
