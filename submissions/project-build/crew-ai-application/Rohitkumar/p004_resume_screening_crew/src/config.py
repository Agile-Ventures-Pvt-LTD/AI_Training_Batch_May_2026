import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = Path(os.getenv("DATASET_PATH", "data/p004_resume_screening_crew_dataset"))
OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH", "outputs"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

JD_PATH = DATASET_PATH / "job_description" / "jd_ai_engineer.md"
RESUMES_DIR = DATASET_PATH / "resumes"
METADATA_DIR = DATASET_PATH / "metadata"
CANDIDATE_INDEX_PATH = METADATA_DIR / "candidate_index.csv"
SCREENING_RUBRIC_PATH = METADATA_DIR / "screening_rubric.json"
SKILL_SYNONYMS_PATH = METADATA_DIR / "skill_synonyms.json"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)