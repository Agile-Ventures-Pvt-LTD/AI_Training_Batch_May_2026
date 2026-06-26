from crewai import Task
from agents import job_review, resume_extraction, Skill_and_Experience_Matching_Agent,Interview_Planning_Agent,Final_Recommendation_Agent


#this is task defined to analyse the job discription
job_review_task = Task(
  description=(
    """
    Read the job discription with the help of tool provided and find the main points required to evaluate candidate,
    pass the job discription path to tool 
    jd_path="data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md"

"""
  ),
  expected_output=(
    """
    Required a well defined json that lists the following
        "role_title"
        "required_skills"
        "preferred_skills"
        "responsibilities"
        "experience_expectation"
        "evaluation_criteria"
"""
  ),
  agent=job_review,
  output_file='Output/jd_analysis.json'
)



#this is task defined to analyse the resume
resume_review_task = Task(
  description=(
    """
    Read the resume with the help of tool provided and find the main points evaluate candidate
    You have the path for resume file, pass it to tool.
    resume_file=
    resume_path="fdata/p004_resume_screening_crew_dataset/resumes/resume_file"
    You will get the resume file name by running tool candidate_index_lookup_tool based on id of candidate

"""
  ),
  expected_output=(
    """
    Required a well defined json that lists the following
        "candidate_id"
        "candidate_name"
        "current_role"
        "years_experience"
        "skills"
        "projects"
        "experience_summary"
        "education"
        "certifications"
        
"""
  ),
  agent=resume_extraction,
  output_file='Output/resume_profile.json'
)




#this is task defined to analyse the candidate against rubric
matching_task = Task(
  description=(
    """
    Read the rubric with the help of tool provided and find the main points evaluate candidate
    You have the path for rubric file, pass it to tool to get rubric for evaluation
    resume_path="data/p004_resume_screening_crew_dataset/metadata/screening_rubric.json"
    Find out the score for candidate against rubric

"""
  ),
  expected_output=(
    """
    Required a well defined json that lists the following
    {
    "matched_skills": [],
    "partial_matches": [],
    "missing_skills": [],
    "category_scores": {
        "python_programming": ,
        "sql_database_skills": ,
        "api_integration": 0,
        "llm_application_development": ,
        "agent_frameworks": ,
        "rag_understanding": ,
        "testing_and_quality": ,
        "communication": 
    },
    "overall_score": ,
    "max_score": 40,
    "percentage": ,
    "recommendation_band": ""
    }
        
        
"""
  ),
  agent=Skill_and_Experience_Matching_Agent,
  context=[resume_review_task],
  output_file='Output/match_score.json'
)




planner_task = Task(
  description=(
    """
    interview need to be planned using the context provided.
    generated required questions and other insights"""
  ),
  expected_output=(
    """
    Required a well defined json that lists the following
    {
        "interview_focus_areas": [],
        "technical_questions": [],
        "project_deep_dive_questions": [],
        "scenario_questions": [],
        "gap_validation_questions": []
      }  
        
"""
  ),
  agent=Interview_Planning_Agent,
  context=[job_review_task,resume_review_task,matching_task],
  output_file='Output/interview_plan.json'
)


final_task = Task(
  description=(
    """
    Based on all the data provided. generate the final report in the required output format.
    take context from previous tasks"""
  ),
  expected_output=(
    """
    Required a well defined json that lists the following
    {
      "candidate_id": "",
      "candidate_name": "",
      "role_title": "",
      "overall_score": ,
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
  agent=Final_Recommendation_Agent,
  context=[job_review_task,resume_review_task,matching_task,planner_task],
  output_file='Output/interview_plan.json'
)