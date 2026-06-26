from crewai import Crew, Process
from agents import (
    jd_analyst,
    resume_extractor,
    skill_matcher,
    interview_planner,
    final_recommender,
)
from tasks import (
    jd_analysis_task,
    resume_extraction_task,
    skill_matching_task,
    interview_planning_task,
    final_report_task,
)

screening_crew = Crew(
    agents=[
        jd_analyst,
        resume_extractor,
        skill_matcher,
        interview_planner,
        final_recommender,
    ],
    tasks=[
        jd_analysis_task,
        resume_extraction_task,
        skill_matching_task,
        interview_planning_task,
        final_report_task,
    ],
    process=Process.sequential,
    verbose=True,
)