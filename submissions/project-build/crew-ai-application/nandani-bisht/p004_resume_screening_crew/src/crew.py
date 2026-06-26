from crewai import Crew, Process
from tasks import (
    get_jd_task,
    get_resume_task,
    get_matching_task,
    get_gap_task,
    get_interview_task,
    get_recommendation_task,
    get_review_task
)

def create_screening_crew(jd_path: str, candidate_id: str):
    tasks = [
        get_jd_task(jd_path),
        get_resume_task(candidate_id),
        get_matching_task(),
        get_gap_task(),
        get_interview_task(),
        get_recommendation_task(candidate_id),
        get_review_task()
    ]
    
    agents = [task.agent for task in tasks]
    
    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        memory=False
    )