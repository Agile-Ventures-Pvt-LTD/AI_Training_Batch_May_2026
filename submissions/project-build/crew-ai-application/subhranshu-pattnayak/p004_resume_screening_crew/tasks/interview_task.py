from crewai import Task
from schemas import InterviewPlan
from agents.interview_planner import interview_planner
from .jd_task import jd_task
from .resume_task import resume_task
from .matching_task import matching_task

interview_task = Task(
    description="""
    Using the Job description, Candidate profile and Skill matching results, generate the interview questions for the candidate for the job requirements.
    Generate the following using the candidate, skill and job information:
    at least 3 technical questions, at least 2 project deep-dive questions, at least 2 scenario questions, at least 2 gap validation questions,
    Focus on generating questions that are not confusing, are well-thought and well phrased.
    Questions should be based on:
    - Job description
    - Candidate profile
    - Skill matching results
    """,
    expected_output="""
    A Structured interview plan including:
    - interview_focus_areas
    - technical_questions
    - project_deep_dive_questions
    - scenario_questions
    - gap_validation_questions
    """,
    agent=interview_planner,
    context=[
        jd_task,
        resume_task,
        matching_task
    ],
    output_pydantic=InterviewPlan
)