from crewai import Agent
from utils.gClient import _default_llm

jd_analyst = Agent(
    role="Job Description Analyst",
    goal=(
        """Analyze the job description and extract structured information about the role, required skills, preferred skills, responsibilities, experience expectations, and evaluation criteria.
        """
    ),
    backstory=("""
        "You are an experienced technical recruiter who specializes in "breaking down job descriptions into structured information that can be used by downstream recruitment systems.
        """
    ),
    llm = _default_llm,
    verbose=True,
    allow_delegation=False
)