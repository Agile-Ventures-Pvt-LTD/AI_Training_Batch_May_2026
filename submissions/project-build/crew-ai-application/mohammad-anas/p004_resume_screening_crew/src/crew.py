from crewai import Crew, Process

from agents import (
    gap_analyst,
    interview_planner,
    jd_analyst,
    recommendation_agent,
    report_reviewer,
    resume_extractor,
    skill_matcher,
)

from tasks import (
    gap_analysis_task,
    interview_planning_task,
    jd_analysis_task,
    recommendation_task,
    report_review_task,
    resume_extraction_task,
    skill_matching_task,
)

resume_screening_crew = Crew(
    agents=[
        jd_analyst,
        resume_extractor,
        skill_matcher,
        gap_analyst,
        interview_planner,
        recommendation_agent,
        report_reviewer,
    ],
    tasks=[
        jd_analysis_task,
        resume_extraction_task,
        skill_matching_task,
        gap_analysis_task,
        interview_planning_task,
        recommendation_task,
        report_review_task,
    ],
    process=Process.sequential,
    verbose=True,
)