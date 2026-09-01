from crewai import Agent, LLM
from src.config import GROQ_MODEL, GROQ_API_KEY
from src.tools import (
    read_job_description_tool,
    read_resume_tool,
    load_screening_rubric_tool,
    score_calculator_tool,
    save_report_tool,
    skill_matcher_tool,
    validate_report_schema_tool
)


llm = LLM(
    model=[GROQ_MODEL, 'meta-llama/llama-4-scout-17b-16e-instruct'],
    provider="openai",
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    temperature=0,
)

def jd_analyst_agent():
    return Agent(
        role="Job Description Analyst",
        goal="Read and analyze the job description to extract the role title, required skills, preferred skills, responsibilities, experience expectations and evaluation criteria",
        backstory="You are an expert job description analyst, your job is to extract clean requirements from job descriptions. ",
        verbose=True,
        allow_delegation=False,
        tools=[read_job_description_tool],
        llm=llm
    )

def resume_extraction_agent() -> Agent:
    return Agent(
        role="Resume Information Extractor",
        goal="Extract structured candidate information from the resume file",
        backstory="You are a expert resume information extractor who specializes in parsing resume documents. You extract factual information from resumes and map them precisely",
        verbose=True,
        allow_delegation=False,
        tools=[read_resume_tool],
        llm=llm
    )

def skill_matching_agent() -> Agent:
    return Agent(
        role="Skill and Experience Matcher",
        goal="Compare the extracted candidate profile with the JD requirements, load the screening rubric and calculate scores for the 8 categories, overall score, percentage and recommendation band",
        backstory="You are a expert skill and experience matching agent. You specialize in comparing resume content to job descriptions. ",
        verbose=True,
        allow_delegation=False,
        tools=[load_screening_rubric_tool, score_calculator_tool, skill_matcher_tool],
        llm=llm
    )

def gap_analysis_agent() -> Agent:
    return Agent(
        role="Gap Analyst",
        goal="Identify critical gaps, moderate gaps and areas to probe between the resume and the job description.",
        backstory="You are a  expert senior interviewer. You are great at finding the gaps, weaknesses in resume and organize them clearly into critical and moderate gaps",
        verbose=True,
        allow_delegation=False,
        tools=[skill_matcher_tool],
        llm=llm
    )

def interview_planning_agent() -> Agent:
    return Agent(
        role="Technical Interview Planner",
        goal="Generate interview questions including technical questions, project deep-dive questions, scenario questions and gap validation questions",
        backstory="You are a expert hiring manager who designs interview questions for each candidate. You make sure questions are for specific claims and gaps in the resume and JD requirements.",
        verbose=True,
        allow_delegation=False,
        tools=[read_job_description_tool],
        llm=llm
    )

def report_reviewer_agent() -> Agent:
    return Agent(
        role="Report Reviewer",
        goal="Review the final report for completeness, schema consistency and evidence quality",
        backstory="You are a report reviewing agent. You check that the final output JSON exactly to the required schemas and review notes on evidence quality",
        verbose=True,
        allow_delegation=False,
        tools=[validate_report_schema_tool],
        llm=llm
    )

def final_recommendation_agent() -> Agent:
    return Agent(
        role="Final Recommendation expert",
        goal="Compile the final screening report ensure it passes schema validation and save the report to the outputs folder",
        backstory="You are the expert lead recruiter. You compile all analysis into the final screening report. You ensure everything is accurate, formatted correctly, validated and saved ",
        verbose=True,
        allow_delegation=False,
        tools=[save_report_tool, validate_report_schema_tool],
        llm=llm
    )
