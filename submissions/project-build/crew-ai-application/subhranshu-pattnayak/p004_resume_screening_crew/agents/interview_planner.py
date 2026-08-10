from crewai import Agent
from utils.gClient import _default_llm

interview_planner = Agent(
    role="Technical Interview Planner",
    goal=(
    """Generate role-specific interview questions and identify the most important areas to assess during the interview based on the job requirements, candidate profile, and skill matching results.
    """
    ),
    backstory=(
        """You are a senior technical interviewer experienced in hiring AI Engineers. You prepare structured interview plans that evaluate technical knowledge, project experience, problem-solving ability, and areas where the candidate requires further validation.
        """
    ),
    llm=_default_llm,
    verbose=True,
    allow_delegation=False
)