from crewai import Task
from tools import 
from agents import blog_researcher, blog_writer
from tools import read_job_description,read_resume_tool,candidate_index_lookup,load_screening_rubric,score_calculator,save_report,skill_matcher_tool
from agents import resume_extraction_agent, job_description_analyst,skill_and_experience_matching_agent,interview_planning_agent,recommendation_agent
# =======================1. job description task=======================================

job_description_task = Task(
  description=(
    "Identity the job description provided by the user"
    "extract the description information from job_description_profile" 
    ""
  ),
  expected_output="""    {
    "candidate_id": "",
    "candidate_name": "",
    "current_role": "",
    "years_experience": "",
    "skills": [],
    "projects": [],
    "experience_summary": [],
    "education": [],
    "certifications": []
    }""",
    tools=[read_job_description]
  agent=job_description_analyst,
  output_file='outputs/jd_analysis.json'

)

resume_extraction_task= Task(
  description=(
    "Take user input and extract the file name of the candidate"
    "based on the file name,extract all the candidate details"
  ),
  expected_output="""    {
    "candidate_id": "",
    "candidate_name": "",
    "current_role": "",
    "years_experience": "",
    "skills": [],
    "projects": [],
    "experience_summary": [],
    "education": [],
    "certifications": []
    }""",
  agent=resume_extraction_agent,
  context=[job_description_task ],
  async_execution=False,
  tools=[candidate_index_lookup,read_resume_tool],
  output_file='outputs/resume_profile.json'  
)


skill_matching_task= Task(
  description=(
    "Compare the candidate details and skill with the job description"
  ),
  expected_output="""    {
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
    }""",
  agent=skill_and_experience_matching_agent,
  context=[job_description_task,resume_extraction_task ],
  async_execution=False,
  tools=[skill_matcher_tool, load_screening_rubric,score_calculator],
  output_file='outputs/match_score.json' 

)


interview_planning_task= Task(
  description=(
    "Compare the candidate details and skill with the job description"
    "the answer should contain Minimum required questions 3 technical questions, 2 project deep-dive questions, 2 scenario questions, 2 gap-validation questions"
    " Generate candidate-specific interview questions."
  ),
  expected_output="""    {
"interview_focus_areas": [],
"technical_questions": [],
"project_deep_dive_questions": [],
"scenario_questions": [],
"gap_validation_questions": []
}
""",
  agent=interview_planning_agent,
  context=[job_description_task,resume_extraction_task,skill_matching_task ],
  async_execution=False,
  tools=[],
  output_file='outputs/interview_plan.json' 

)


recommendation_task= Task(
  description=(
    "Produce final screening result"
    "provide recommendation as STRONG_MATCH | MODERATE_MATCH | WEAK_MATCH | NEEDS_MANUAL_REVIEW based on screening and analysing "
  ),
  expected_output="""    {
"interview_focus_areas": [],
"technical_questions": [],
"project_deep_dive_questions": [],
"scenario_questions": [],
"gap_validation_questions": []
}
""",
  agent=interview_planning_agent,
  context=[job_description_task,resume_extraction_task,skill_matching_task,interview_planning_task],
  async_execution=False,
  tools=[save_report],
  output_file='outputs/candidate_screening_report.json' 

)