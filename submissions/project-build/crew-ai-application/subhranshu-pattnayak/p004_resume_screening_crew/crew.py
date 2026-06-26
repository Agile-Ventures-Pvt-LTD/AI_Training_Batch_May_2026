from crewai import Crew, Process

from agents.jd_analyst import jd_analyst
from agents.resume_extractor import resume_extractor
from agents.skill_matcher import matching_agent
from agents.interview_planner import interview_planner
from agents.report_writer import report_writer

from tasks.jd_task import jd_task
from tasks.resume_task import resume_task
from tasks.matching_task import matching_task
from tasks.interview_task import interview_task
from tasks.report_task import report_task


resume_screening_crew = Crew(
    agents=[
        jd_analyst,
        resume_extractor,
        matching_agent,
        interview_planner,
        report_writer,
    ],
    tasks=[
        jd_task,
        resume_task,
        matching_task,
        interview_task,
        report_task,
    ],
    process=Process.sequential,
    verbose=True,
)