# crew.py
from crewai import Crew, Process

from agents import (
    jd_analyst_agent,
    resume_extractor_agent,
    matching_agent,
    interview_planner_agent,
    recommendation_agent
)
from tasks import (
    task_analyze_jd,
    task_extract_resume,
    task_match_skills,
    task_plan_interview,
    task_generate_report
)

def build_screening_crew() -> Crew:

    return Crew(
        agents=[
            jd_analyst_agent,
            resume_extractor_agent,
            matching_agent,
            interview_planner_agent,
            recommendation_agent
        ],
        tasks=[
            task_analyze_jd,
            task_extract_resume,
            task_match_skills,
            task_plan_interview,
            task_generate_report
        ],
        process=Process.sequential,
        verbose=True,
        memory=True
    )
