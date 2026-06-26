from crewai import Crew
from crewai import Process

from agents.agents import(
    job_description_analyst_agent,
    resume_extraction_agent,
    skill_and_experience_matching_agent, 
    interview_planning_agent,
    final_recommendation_agent,
    gap_analysis_agent,
    report_review_agent

)

from tasks.tasks import (
    description_analyst_task,
    extraction_task,
    skill_experience_matching_task,
    interview_planning_task,
    recommendation_task,
    gap_analysis_task,
    report_review_task
)

from tools.tools import TOOLS(
    read_job_description,
    read_resume,
    candidate_screening_lookup,
    load_screening_rubric,
    score_calculator,
    save_report_tool

)

def ai_resume_screening_and_interview_planning(project_name):
    analyst = job_description_analyst_agent()
    extraction = resume_extraction_agent()
    matching = skill_and_experience_matching_agent()
    interview = interview_planning_agent()
    recommendation = final_recommendation_agent()
    gap = gap_analysis_agent()
    review = report_review_agent()

    task1 = description_analyst_task(
        analyst,
        project_name
    )
    task2 = extraction_task(
        extraction,
        project_name
    )
    task3 = skill_experience_matching_task(
        matching,
        project_name
    )
    task4 = interview_planning_task(
        interview,
        project_name
    )
    task5 = recommendation_task(
        recommendation,
        project_name
    )
    task6 = gap_analysis_task(
        gap,
        project_name
    )
    task7 = report_review_task(
        review,
        project_name
    )
    crew = Crew(
        agents = [
            analyst,
            extraction,
            matching,
            interview,
            recommendation,
            gap,
            review
        ],
        tasks = [
            task1,
            task2, 
            task3, 
            task4, 
            task5,
            task6,
            task7
        ],
        process = Process.sequential,
        verbose=True
    )
    return crew