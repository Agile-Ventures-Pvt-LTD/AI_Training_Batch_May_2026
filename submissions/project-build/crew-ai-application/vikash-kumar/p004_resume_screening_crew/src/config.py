
import os
from dotenv import load_dotenv
load_dotenv()
from crewai import LLM


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"],
    tool_choice="auto"
    )


DEFAULT_TEMPERATURE = 0.3
MAX_TOKENS = 3000
REQUEST_TIMEOUT = 60


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL","openai/gpt-oss-120b") #llama-3.3-70b-versatile
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
os.environ["CONFIDENT_API"] = os.getenv("CONFIDENT_API_KEY")

JOB_DESCRIPTION_PATH =  os.getenv("JOB_DESCRIPTION_PATH","data/p004_resume_screening_crew_dataset/job_description")
CANDIDATE_INDEX_PATH = os.getenv("CANDIDATE_INDEX_PATH","data/p004_resume_screening_crew_dataset/metadata/candidate_index.csv")
SCREENING_RUBRIC_PATH = os.getenv("SCREENING_RUBRIC_PATH","data/p004_resume_screening_crew_dataset/metadata/screening_rubric.json")
SKILLS_SYNONYMS_PATH = os.getenv("SKILLS_SYNONYMS_PATH","data/p004_resume_screening_crew_dataset/metadata/skill_synonyms.json")
RESUME_PATH = os.getenv("RESUME_PATH","data/p004_resume_screening_crew_dataset/resumes")

SCREENING_SUPPORT_INDICATORS=[
    "STRONG_MATCH",
    "MODERATE_MATCH",
    "WEAK_MATCH",
    "NEEDS_MANUAL_REVIEW"
]
