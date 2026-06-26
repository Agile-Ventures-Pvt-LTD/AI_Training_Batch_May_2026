from src.config import llm
from crewai import Agent
from src.tools import (
    read_job_description,
    read_resume_tool,
    candidate_index_lookup_tool,
    load_screening_rubric_tool,
    score_calculator_tool,
    skill_matcher_tool,
    save_report_tool,
    validate_report_schema_tool
)


manager = Agent(
    role="Manager Of the Process",
    goal="Understand the Query and call the different agent",
    backstory="You are good at assign the task to other agents.",
    allow_delegation=True,
    llm=llm,
    memory=True
)


job_description = Agent(
    role="Job Description Analyst",
    goal="Understand the job description.",
    backstory="You are good at describing the job description",
    allow_delegation=True,
    tools=[read_job_description],
    llm=llm,
    memory=True
)


resume_extraction = Agent(
    role="Resume Extraction",
    goal="Extract structured candidate information from the resume.",
    backstory="You are good at extracting the resumes from the folder",
    allow_delegation=True,
    tools=[candidate_index_lookup_tool, read_resume_tool],
    llm=llm,
    memory=True
)


experience_matching = Agent(
    role="Skill and Experience Matching",
    goal="Compare JD requirements with the candidate profile.",
    backstory="You compare the job description and the candidate profile for the skills and experience match",
    allow_delegation=True,
    tools=[read_job_description, candidate_index_lookup_tool, read_resume_tool, load_screening_rubric_tool, score_calculator_tool, skill_matcher_tool],
    llm=llm,
    memory=True
)


interview_planning = Agent(
    role="Interview Planning",
    goal="Generate candidate-specific interview questions.",
    backstory="you are good at making the interview questions according to the candidate profile",
    allow_delegation=True,
    tools=[read_job_description, read_resume_tool, candidate_index_lookup_tool, score_calculator_tool],
    llm=llm,
    memory=True,
)


final_recommendation = Agent(
    role="Final Recommendation",
    goal="Produce the final screening report",
    backstory="You are good at making the reports by analayzing the candidate profile",
    allow_delegation=True,
    tools=[read_job_description, read_resume_tool, candidate_index_lookup_tool, load_screening_rubric_tool, score_calculator_tool, skill_matcher_tool, save_report_tool, validate_report_schema_tool],
    llm=llm,
    memory=True
)


gap_analysis = Agent(
    role="Gap Analysist",
    goal="Identify missing or weak areas separately.",
    backstory="You are good at identifying the missing and weak areas of the candidate using the candidate information",
    allow_delegation=True,
    llm=llm,
    memory=True,
)


report_review = Agent(
    role="Report Reviewer",
    goal="Review final report for completeness, schema consistency, and evidence quality.",
    backstory="You are good at reviewing the markdown files with all the given evidence",
    allow_delegation=True,
    tools=[validate_report_schema_tool],
    llm=llm,
    memory=True
)