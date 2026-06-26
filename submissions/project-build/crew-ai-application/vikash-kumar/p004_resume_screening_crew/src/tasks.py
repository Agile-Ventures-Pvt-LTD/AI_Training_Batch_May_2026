from crewai import LLM, Agent, Task, Crew, Process
from agents import job_decription_analyst,resume_extraction,skill_and_experience_matching,report_review,gap_analysis,final_recommendation,interview_planning_agent
from schemas import jd_schema_analyst_output_schema,resume_extraction_output_schema,skill_matching_output_schmea,interview_planning_output_schmea,final_recommendation_output_schema,gap_analysis_output_schema,agent_review_output_schmea

jd_analyst_task = Task(
  description=("""Undestand the job description
               Inputs: jd_ai_engineer.md"""
   ),
  expected_output=(
   """
The expected output is the following format:
{"role_title": "",
"required_skills": [],
"preferred_skills": [],
"responsibilities": [],
"experience_expectation": "",
"evaluation_criteria": []}""" ),
  agent=job_decription_analyst # Assign this task to our support agent
)


resume_extraction_task = Task(
  description=("""Extract structured candidate information from the resume.
               Inputs: candidate resume file"""
   ),
  expected_output=(
   """
The expected output is the following format:
{
"candidate_id": "",
"candidate_name": "",
"current_role": "",
"years_experience": "",
"skills": [],
"projects": [],
"experience_summary": [],
"education": [],
"certifications": []}""" ),
  agent=resume_extraction # Assign this task to our support agent
)
#############################
skill_and_experience_matching_task = Task(
  description=("""Compare JD requirements with the candidate profile
               Inputs:
jd_analysis.json
resume_profile.json
screening_rubric.json
skill_synonyms.json
"""
   ),
  expected_output=(
   """
The expected output is the following format:
{"matched_skills": [],
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
"recommendation_band": ""}""" ),
  agent=skill_and_experience_matching # Assign this task to our support agent
)


interview_planning_agent_task = Task(
  description=("""Generate candidate-specific interview questions.
Inputs:
jd_analysis.json
resume_profile.json
match_score.json"""
   ),
  expected_output=(
   """
The expected output is the following format:
{"interview_focus_areas": [],
"technical_questions": [],
"project_deep_dive_questions": [],
"scenario_questions": [],
"gap_validation_questions": []}""" ),
  agent=interview_planning_agent # Assign this task to our support agent
)


final_recommendation_task = Task(
  description=("""Produce the final screening report.
Inputs:
jd_analysis.json
resume_profile.json
match_score.json
interview_plan.json"""
   ),
  expected_output=(
   """
The expected output is the following format:
{"candidate_id": "",
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
"human_review_note": ""}""" ),
  agent=final_recommendation # Assign this task to our support agent
)


gap_analysis_task = Task(
  description=(""" Identify missing or weak areas separately."""
   ),
  expected_output=(
   """
The expected output is the following format:
{
"critical_gaps": [],
"moderate_gaps": [],
"areas_to_probe": []}""" ),
  agent=gap_analysis # Assign this task to our support agent
)
##############################



report_review_task = Task(
  description=(""" Review final report for completeness, schema consistency, and 
evidence quality."""
   ),
  expected_output=(
   """
The expected output is the following format:
{
"report_complete": true,
"missing_sections": [],
"schema_valid": true,
"review_notes": []}""" ),
  agent=report_review # Assign this task to our support agent
)