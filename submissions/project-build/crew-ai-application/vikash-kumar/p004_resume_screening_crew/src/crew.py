from crewai import LLM, Agent, Task, Crew, Process

from agents import job_decription_analyst,resume_extraction,skill_and_experience_matching,report_review,gap_analysis,final_recommendation,interview_planning_agent
from tasks import jd_analyst_task,resume_extraction_task,skill_and_experience_matching_task,interview_planning_agent_task,final_recommendation_task,gap_analysis_task,report_review_task

screening_crew = Crew(
  agents=[job_decription_analyst,resume_extraction,skill_and_experience_matching,report_review,gap_analysis,final_recommendation,interview_planning_agent],
  tasks=[jd_analyst_task,resume_extraction_task,skill_and_experience_matching_task,interview_planning_agent_task,final_recommendation_task,gap_analysis_task,report_review_task],
    process=Process.sequential, # Tasks execute one after another (only one task here)
  verbose=True
)