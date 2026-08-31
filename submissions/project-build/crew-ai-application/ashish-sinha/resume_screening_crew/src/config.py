import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"],
    tool_choice="auto",
    max_tokens=4000
    )

base_path = os.getenv("DATASET_PATH", "data/p004_resume_screening_crew_dataset")
jd_path = os.path.join(base_path, "job_description/jd_ai_engineer.md")
OUTPUT_PATH = os.getenv('OUTPUT_PATH', 'outputs')

def get_resume_path(resume_file: str) -> str:
    """Constructs the complete path for a given candidate resume filename."""
    return os.path.join(base_path, "resumes", resume_file)
