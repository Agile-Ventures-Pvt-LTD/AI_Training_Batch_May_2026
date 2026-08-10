from crewai import Agent
from config import llm
from tools import (
    read_job_description_tool,
    read_resume_tool,
    candidate_index_lookup_tool,
    load_screening_rubric_tool,
    skill_matcher_tool,
    score_calculator_tool,
    validate_report_schema_tool,
    save_report_tool
)

def get_jd_analyst():
    return Agent(
        role="Job Description Analyst",
        goal="Extract structured requirements, skills, and evaluation criteria from the job description.",
        backstory="Expert technical recruiter specializing in parsing complex job descriptions into standardized evaluation matrices.",
        llm=llm,
        tools=[read_job_description_tool],
        allow_delegation=False,
        verbose=True
    )

def get_resume_extractor():
    return Agent(
        role="Resume Extraction Specialist",
        goal="Extract structured candidate profile data including skills, experience, and projects from the resume.",
        backstory="Detail-oriented HR analyst with a focus on accurately mapping unstructured resume text to standardized candidate profiles without hallucinating missing information.",
        llm=llm,
        tools=[read_resume_tool, candidate_index_lookup_tool],
        allow_delegation=False,
        verbose=True
    )

def get_skill_matcher():
    return Agent(
        role="Skill and Experience Matcher",
        goal="Compare candidate skills against JD requirements, calculate category scores, and determine the recommendation band.",
        backstory="Analytical talent assessor who strictly applies scoring rubrics and uses deterministic tools to calculate match percentages and identify skill gaps.",
        llm=llm,
        tools=[load_screening_rubric_tool, skill_matcher_tool, score_calculator_tool],
        allow_delegation=False,
        verbose=True
    )

def get_gap_analyst():
    return Agent(
        role="Gap Analysis Expert",
        goal="Identify critical and moderate gaps in the candidate's profile relative to the job requirements.",
        backstory="Critical thinker who evaluates missing skills and experience to highlight specific areas that require probing during interviews.",
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

def get_interview_planner():
    return Agent(
        role="Interview Planning Strategist",
        goal="Generate targeted technical, project, scenario, and gap-validation interview questions.",
        backstory="Senior engineering interviewer who designs questions specifically tailored to validate claimed skills and probe identified gaps.",
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

def get_final_recommender():
    return Agent(
        role="Final Recommendation Synthesizer",
        goal="Compile all analyses into a comprehensive, evidence-backed final screening report.",
        backstory="Hiring committee lead who synthesizes diverse data points into clear, actionable executive summaries and final recommendations.",
        llm=llm,
        tools=[save_report_tool],
        allow_delegation=False,
        verbose=True
    )

def get_report_reviewer():
    return Agent(
        role="Report Quality Reviewer",
        goal="Validate the final report for schema compliance, completeness, and evidence quality.",
        backstory="QA specialist for hiring operations ensuring all generated reports meet strict organizational standards before human review.",
        llm=llm,
        tools=[validate_report_schema_tool],
        allow_delegation=False,
        verbose=True
    )