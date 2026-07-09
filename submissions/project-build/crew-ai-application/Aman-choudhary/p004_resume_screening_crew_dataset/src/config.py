
from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()
ROOT_DIR = Path(__file__).resolve().parent.parent
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")
DATASET_PATH = Path(os.getenv("DATASET_PATH",ROOT_DIR / "data" / "p004_resume_screening_crew_dataset"))
JOB_DESCRIPTION_DIR = (DATASET_PATH / "job_description")
JOB_DESCRIPTION_FILE = (JOB_DESCRIPTION_DIR / "jd_ai_engineer.md")
RESUMES_DIR = (DATASET_PATH / "resumes")
METADATA_DIR = (DATASET_PATH / "metadata")
CANDIDATE_INDEX_FILE = (METADATA_DIR / "candidate_index.csv")
SCREENING_RUBRIC_FILE = (METADATA_DIR / "screening_rubric.json")
SKILL_SYNONYMS_FILE = (METADATA_DIR / "skill_synonyms.json")
OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH",ROOT_DIR / "outputs"))
OUTPUT_PATH.mkdir(parents=True,exist_ok=True)
EXECUTION_LOG_FILE = (OUTPUT_PATH / "execution_log.txt")
MAX_CATEGORY_SCORE = 5
MAX_TOTAL_SCORE = 40
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
STRONG_MATCH = "STRONG_MATCH"
MODERATE_MATCH = "MODERATE_MATCH"
WEAK_MATCH = "WEAK_MATCH"
NEEDS_MANUAL_REVIEW = "NEEDS_MANUAL_REVIEW"
HUMAN_REVIEW_NOTE = (
    "This is an AI-assisted screening report based on the "
    "provided resume and job description. "
    "A human reviewer should validate the recommendation "
    "before making any recruitment decision."
)
def validate_config() -> None:
    """
    Validate critical configuration.
    """
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset path not found: {DATASET_PATH}"
        )
    if not CANDIDATE_INDEX_FILE.exists():
        raise FileNotFoundError(
            f"Candidate index missing: "
            f"{CANDIDATE_INDEX_FILE}"
        )
    if not SCREENING_RUBRIC_FILE.exists():
        raise FileNotFoundError(
            f"Rubric file missing: "
            f"{SCREENING_RUBRIC_FILE}"
        )
    if not SKILL_SYNONYMS_FILE.exists():
        raise FileNotFoundError(
            f"Skill synonym file missing: "
            f"{SKILL_SYNONYMS_FILE}"
        )

if __name__ == "__main__":
    validate_config()
    print("Configuration Loaded")
    print(f"Dataset: {DATASET_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Model: {GROQ_MODEL}")