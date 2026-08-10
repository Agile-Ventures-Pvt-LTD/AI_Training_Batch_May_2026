from crewai import Task
from schemas import ResumeProfile
from agents.resume_extractor import resume_extractor
from tools.candidate_lookup import candidate_lookup
from tools.read_resume import read_resume


resume_task = Task(
    description=f"""
    Using the candidate id that are in form CAND-001, CAND-002, etc. locate the candidate resume using the candidate ID. 
    Using the path found read the resume.
    Extract the following information from it:
    Candidate ID, Candidate Name, Current Role, Years of Experience, Skills, Projects, Experience Summary, Education, Certifications
    Do not invent any information.
    Focus on finding relevant data.
    Focus on analyzing the job description and getting data that is not misleading or not present in job description.
    Return only structured information.
    """,

    expected_output="""
    A Structured resume profile including:
    - Candidate ID
    - Candidate Name
    - Current Role
    - Years of Experience
    - Skills
    - Projects
    - Experience Summary
    - Education
    - Certifications
    """,
    agent=resume_extractor,
    tools=[candidate_lookup, read_resume],
    output_pydantic=ResumeProfile
)