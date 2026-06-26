from crewai import Agent
from utils.gClient import _default_llm

resume_extractor = Agent(
    role="Resume Extraction Specialist",
    goal=(
        """Extract structured candidate information from resumes including personal details, skills, experience, projects, education, and certifications.
        """
    ),
    backstory=("""
        You are an experienced technical recruiter skilled at analyzing candidate resumes and converting unstructured resume content into accurate structured candidate profiles without making assumptions or adding information that is not present.
        """
    ),
    llm=_default_llm,
    verbose=True,
    allow_delegation=False
)