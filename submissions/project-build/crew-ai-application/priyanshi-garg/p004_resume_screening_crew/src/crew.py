from crewai import Crew, Process
from agents import (
    job_description_analyst, resume_extraction_agent, skill_experience_matching_agent,
    gap_analysis_agent, interview_planning_agent, final_recommendation_agent, report_review_agent
)
from tasks import (
    analyze_jd_task, extract_resume_task, match_skills_task,
    gap_analysis_task, plan_interview_task, generate_report_task, review_report_task
)

def create_screening_crew() -> Crew:
    """Combines pre-defined agents and tasks into a sequential screening crew."""
    return Crew(
        agents=[
            job_description_analyst, 
            resume_extraction_agent, 
            skill_experience_matching_agent,
            gap_analysis_agent, 
            interview_planning_agent, 
            final_recommendation_agent, 
            report_review_agent
        ],
        tasks=[
            analyze_jd_task, 
            extract_resume_task, 
            match_skills_task,
            gap_analysis_task, 
            plan_interview_task, 
            generate_report_task, 
            review_report_task
        ],
        process=Process.sequential,
        verbose=True
    )
