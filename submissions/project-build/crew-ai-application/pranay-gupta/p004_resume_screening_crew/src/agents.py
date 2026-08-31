from crewai import Agent, LLM
from src.config import GROQ_API_KEY, GROQ_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from src.tools import (
    read_job_description_tool, read_resume_tool, candidate_index_lookup_tool,
    load_screening_rubric_tool, score_calculator_tool, save_report_tool,
    skill_matcher_tool, validate_report_schema_tool
)

llm = LLM(
    model=f"groq/{GROQ_MODEL}",
    api_key=GROQ_API_KEY,
    temperature=LLM_TEMPERATURE,
    max_tokens=LLM_MAX_TOKENS,
    drop_params=True  # Forces LiteLLM to drop unsupported parameters like cache_breakpoint
)

jd_analyst_agent = Agent(
    role="Job Description Analyst",
    goal="Extract role title, required skills, and responsibilities from the JD.",
    backstory="A senior technical recruiter who identifies explicit and implicit requirements.",
    llm=llm,
    tools=[read_job_description_tool],
    allow_delegation=False,
    verbose=True
)

resume_extraction_agent = Agent(
    role="Resume Extraction Specialist",
    goal="Extract structured candidate info from the resume.",
    backstory="An expert resume parser who extracts only factual information without assumptions.",
    llm=llm,
    tools=[read_resume_tool],
    allow_delegation=False,
    verbose=True
)

skill_matching_agent = Agent(
    role="Skill and Experience Matching Analyst",
    goal="Compare JD with resume and score 8 rubric categories.",
    backstory="A technical assessor who scores strictly based on evidence. Never gives 5 without projects.",
    llm=llm,
    tools=[load_screening_rubric_tool, skill_matcher_tool, score_calculator_tool],
    allow_delegation=False,
    verbose=True
)

gap_analysis_agent = Agent(
    role="Gap Analysis Specialist",
    goal="Identify critical and moderate gaps in the candidate profile.",
    backstory="A hiring manager focused on risk areas and interview probing topics.",
    llm=llm,
    tools=[],
    allow_delegation=False,
    verbose=True
)

interview_planning_agent = Agent(
    role="Interview Planning Specialist",
    goal="Generate tailored interview questions based on gaps and projects.",
    backstory="A senior engineering manager who designs structured interviews.",
    llm=llm,
    tools=[],
    allow_delegation=False,
    verbose=True
)

final_recommendation_agent = Agent(
    role="Final Recommendation and Report Generator",
    goal="Synthesize all outputs into the final JSON report and save it.",
    backstory="A lead recruiter who writes evidence-backed reports. Never invents information.",
    llm=llm,
    tools=[save_report_tool, validate_report_schema_tool],
    allow_delegation=False,
    verbose=True
)

report_review_agent = Agent(
    role="Report Quality Reviewer",
    goal="Verify report completeness and schema validity.",
    backstory="A QA specialist ensuring reports meet quality standards before reaching managers.",
    llm=llm,
    tools=[validate_report_schema_tool],
    allow_delegation=False,
    verbose=True
)

ALL_AGENTS = [
    jd_analyst_agent,
    resume_extraction_agent,
    skill_matching_agent,
    gap_analysis_agent,
    interview_planning_agent,
    final_recommendation_agent,
    report_review_agent,
]