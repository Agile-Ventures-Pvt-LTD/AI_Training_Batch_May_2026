from crewai import Agent
from crewai import Agent, LLM

import config

from prompts.gap_analysis import SYSTEM_PROMPT as GAP_PROMPT
from prompts.interview_planner import SYSTEM_PROMPT as INTERVIEW_PROMPT
from prompts.jd_analyst import SYSTEM_PROMPT as JD_PROMPT
from prompts.recommendation import SYSTEM_PROMPT as RECOMMENDATION_PROMPT
from prompts.report_reviewer import SYSTEM_PROMPT as REVIEW_PROMPT
from prompts.resume_extractor import SYSTEM_PROMPT as RESUME_PROMPT
from prompts.skill_matcher import SYSTEM_PROMPT as MATCHER_PROMPT

from tools import (
    load_screening_rubric_tool,
    read_job_description_tool,
    read_resume_tool,
    save_report_tool,
    score_calculator_tool,
    skill_matcher_tool,
    validate_report_schema_tool,
)

llm = LLM(
    model=f"groq/{config.GROQ_MODEL}",
    api_key=config.GROQ_API_KEY,
    temperature=config.TEMPERATURE,
)

jd_analyst = Agent(
    role="Job Description Analyst",
    goal="Analyze the job description.",
    backstory=JD_PROMPT,
    llm=llm,
    tools=[
        read_job_description_tool,
    ],
    verbose=True,
)

resume_extractor = Agent(
    role="Resume Extractor",
    goal="Extract candidate profile.",
    backstory=RESUME_PROMPT,
    llm=llm,
    tools=[
        read_resume_tool,
    ],
    verbose=True,
)

skill_matcher = Agent(
    role="Skill Matcher",
    goal="Compare candidate against the job description.",
    backstory=MATCHER_PROMPT,
    llm=llm,
    tools=[
        skill_matcher_tool,
        load_screening_rubric_tool,
        score_calculator_tool,
    ],
    verbose=True,
)

gap_analyst = Agent(
    role="Gap Analyst",
    goal="Identify candidate gaps.",
    backstory=GAP_PROMPT,
    llm=llm,
    verbose=True,
)

interview_planner = Agent(
    role="Interview Planner",
    goal="Generate interview questions.",
    backstory=INTERVIEW_PROMPT,
    llm=llm,
    verbose=True,
)

recommendation_agent = Agent(
    role="Recommendation Agent",
    goal="Generate hiring recommendation.",
    backstory=RECOMMENDATION_PROMPT,
    llm=llm,
    tools=[
        save_report_tool,
    ],
    verbose=True,
)

report_reviewer = Agent(
    role="Report Reviewer",
    goal="Validate the final report.",
    backstory=REVIEW_PROMPT,
    llm=llm,
    tools=[
        validate_report_schema_tool,
    ],
    verbose=True,
)