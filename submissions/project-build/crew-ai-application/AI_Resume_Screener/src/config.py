import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

# LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Paths — resolved relative to project root regardless of cwd
_PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATASET_PATH = str(_PROJECT_ROOT / os.getenv("DATASET_PATH", "data/dataset"))
OUTPUT_PATH = str(_PROJECT_ROOT / os.getenv("OUTPUT_PATH", "outputs"))

JD_PATH = os.path.join(DATASET_PATH, "job_description/jd_ai_engineer.md")
RESUMES_PATH = os.path.join(DATASET_PATH, "resumes")
CANDIDATE_INDEX_PATH = os.path.join(DATASET_PATH, "metadata/candidate_index.csv")
SCREENING_RUBRIC_PATH = os.path.join(DATASET_PATH, "metadata/screening_rubric.json")
SKILL_SYNONYMS_PATH = os.path.join(DATASET_PATH, "metadata/skill_synonyms.json")

# Required candidates
REQUIRED_CANDIDATES = ["CAND-001", "CAND-002", "CAND-003"]
ALL_CANDIDATES = ["CAND-001", "CAND-002", "CAND-003", "CAND-004", "CAND-005"]