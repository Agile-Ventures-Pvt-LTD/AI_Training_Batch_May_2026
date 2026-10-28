from crewai import Crew, Process
from src.agents import (
    manager,
    job_description,
    resume_extraction,
    experience_matching,
    interview_planning,
    final_recommendation,
    gap_analysis,
    report_review
)
from src.tasks import (
    manager_task,
    job_description_task,
    resume_extraction_task,
    experience_matching_task,
    interview_planning_task,
    final_recommendation_task,
    gap_analysis_task,
    report_review_task
)


resume_screening_crew = Crew(
    agents=[manager, job_description, resume_extraction, experience_matching, interview_planning, final_recommendation, gap_analysis, report_review],
    tasks=[manager_task, job_description_task, resume_extraction_task, experience_matching_task, interview_planning_task, final_recommendation_task, gap_analysis_task, report_review_task],
    process=Process.sequential,
    # verbose=True  # For development only 
)