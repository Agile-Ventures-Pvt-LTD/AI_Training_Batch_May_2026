import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "8192"))

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / os.getenv("DATASET_PATH", "data/p004_resume_screening_crew_dataset")
OUTPUT_PATH = PROJECT_ROOT / os.getenv("OUTPUT_PATH", "outputs")

JD_DIR = DATASET_PATH / "job_description"
RESUMES_DIR = DATASET_PATH / "resumes"
METADATA_DIR = DATASET_PATH / "metadata"

JD_FILE_PATH = JD_DIR / "jd_ai_engineer.md"
CANDIDATE_INDEX_PATH = METADATA_DIR / "candidate_index.csv"
SCREENING_RUBRIC_PATH = METADATA_DIR / "screening_rubric.json"
SKILL_SYNONYMS_PATH = METADATA_DIR / "skill_synonyms.json"

MAX_SCORE = 40
RUBRIC_CATEGORIES = [
    "python_programming",
    "sql_database_skills",
    "api_integration",
    "llm_application_development",
    "agent_frameworks",
    "rag_understanding",
    "testing_and_quality",
    "communication",
]

HUMAN_REVIEW_NOTE = (
    "This is an AI-assisted screening report based on the provided resume "
    "and job description. A human reviewer should validate the "
    "recommendation before making any recruitment decision."
)

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

def get_resume_path(resume_filename: str) -> Path:
    return RESUMES_DIR / resume_filename

def get_output_report_path(candidate_id: str) -> Path:
    return OUTPUT_PATH / f"{candidate_id}_screening_report.json"

def get_output_md_path(candidate_id: str) -> Path:
    return OUTPUT_PATH / f"{candidate_id}_screening_report.md"