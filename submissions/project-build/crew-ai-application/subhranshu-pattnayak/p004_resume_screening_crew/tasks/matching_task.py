from crewai import Task
from schemas import MatchScore
from .jd_task import jd_task
from .resume_task import resume_task
from agents.skill_matcher import matching_agent
from tools.load_rubric import load_rubric
from tools.skill_matcher import skill_matcher
from tools.scoring import calculate_score


matching_task = Task(
    description="""
    Using the jd_task and resume_task, compare the candidate profile with the job requirements.
    Use the screening rubric to do it and identifying:
    matched skills, partial matches, missing skills
    Focus on matching skills using tools and context provided and calculating score for every rubric category.
    Calculate: overall score, percentage, recommendation band,
    Base every decision only on the provided resume.
    """,
    expected_output="""
    A Candidate matching report including:
    - matched_skills
    - partial_matches
    - missing_skills
    - category_score
    - overall_score
    - max_score
    - percentage
    - recommendation_band
    """,
    agent=matching_agent,
    context=[
        jd_task,
        resume_task
    ],
    tools=[
        load_rubric,
        skill_matcher,
        calculate_score
    ],
    output_pydantic=MatchScore
)
