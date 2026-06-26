from crewai.agent import Agent
from tools import (read_job_description_tool,
read_resume_tool,
candidate_index_lookup_tool,
load_screening_rubric_tool,
skill_matcher_tool,
validate_report_schema_tool)
from config import llm
from output_writer import save_report_tool
from scoring import score_calculator_tool

job_description_analyst = Agent(
    role="Job Description Analyst",
    goal="Thoroughly analyze the job description to extract structured requirements.",
    backstory="...",
    tools=[read_job_description_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False
)



resume_extraction_agent = Agent(
    role="Resume Extraction Specialist",
    goal="Extract and structure clean, complete profile data from candidate resumes.",
    backstory=(
        "You are an expert HR data specialist. You have an eye for detail and "
        "transform raw, unformatted resume text into highly structured JSON formats. "
        "You always extract exact skills, clear timelines, and explicit details "
        "without skipping any professional achievements or project details."
    ),
    tools=[candidate_index_lookup_tool, read_resume_tool],
    verbose=True,
    llm=llm,
    allow_delegation=False
)

skill_experience_matching_agent = Agent(
    role="Skill and Experience Matcher",
    goal="Quantify alignment between job requirements and candidate profiles using strict scoring rubrics.",
    backstory=(
        "You are a rigorous technical assessment auditor. You excel at comparing "
        "extracted candidate profiles against explicit job requirements. Using standardized rubrics "
        "and data tools, you calculate exact objective performance scores, map skill synonym overlaps, "
        "and determine categorical evaluations without introducing personal bias."
    ),
    tools=[load_screening_rubric_tool, skill_matcher_tool, score_calculator_tool],
    verbose=True,
    llm=llm,
    allow_delegation=False
)


interview_planning_agent = Agent(
    role="Interview Planning Strategist",
    goal="Generate customized, high-signal interview questions tailored to candidate gaps and project history.",
    backstory=(
        "You are an elite technical interview designer. You specialize in analyzing "
        "missing skills, project architectures, and candidate profile gaps to build "
        "hyper-targeted technical evaluations. You ensure every question extracts maximum "
        "signal while strictly meeting structural counts."
    ),
    tools=[],
    verbose=True,
    llm=llm,
    allow_delegation=False
)

final_recommendation_agent = Agent(
    role="Final Recommendation Authority",
    goal="Consolidate all screening artifacts into a unified, validated master screening report.",
    backstory="Chief Talent Officer synthesizing multi-agent feedback streams into a clear programmatic verdict.",
    tools=[
       validate_report_schema_tool, 
       save_report_tool
    ],
    llm=llm,
    allow_delegation=False,
    verbose=True
)

gap_analysis_agent = Agent(
    role="Gap Analysis Specialist",
    goal="Isolate, categorize, and deeply analyze missing or weak qualifications in candidate profiles.",
    backstory=(
        "You are an elite technical gap auditor. You look past surface-level matches "
        "to pinpoint exactly where a candidate falls short of requirements. You "
        "categorize these variances into clear severity tiers so interviewers know "
        "exactly what risks exist."
    ),
    tools=[], 
    verbose=True,
    llm=llm,
    allow_delegation=False
)


report_review_agent = Agent(
    role="Quality Assurance Report Reviewer",
    goal="Audit the final screening reports for strict schema consistency, data completeness, and evidence quality.",
    backstory=(
        "You are a rigorous Quality Assurance Auditor. You possess an eagle eye for "
        "missing fields, logical discrepancies, and weak textual evidence. You ensure that "
        "no screening report is finalized unless it is 100 percent accurate, complete, and fully "
        "substantiated by the candidate's actual history."
    ),
    tools=[validate_report_schema_tool],
    verbose=True,
    llm=llm,
    allow_delegation=False
)

