from crewai import Task
from schemas import JDAnalysis
from agents.jd_analyst import jd_analyst
from tools.read_job_description import read_job_description
from config import DATASET_PATH

jd_path = DATASET_PATH / "job description" / "jd_ai_engineer.md"


jd_task = Task(
    description=f"""
    Using the provided job description at the location {jd_path}, 
    Extract the following information: 
    Role title, Required skills, Preferred skills, Responsibilities, Experience expectation, Evaluation criteria
    Focus on finding relevant data.
    Focus on analyzing the job description and getting data that is not misleading or not present in job description.
    Return only structured information.
    """,
    expected_output="""
    A Structured job description analysis that includes:
    - role_title 
    - required_skills 
    - preferred_skills 
    - responsibilities 
    - experience_expectation 
    - evaluation_criteria
    """,
    agent=jd_analyst,
    tools=[read_job_description],
    output_pydantic=JDAnalysis
)
