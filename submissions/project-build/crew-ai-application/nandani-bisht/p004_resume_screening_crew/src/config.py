import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "groq/llama-3.3-70b-versatile")
DATASET_PATH = BASE_DIR / os.getenv("DATASET_PATH", "data/p004_resume_screening_crew_dataset")
OUTPUT_PATH = BASE_DIR / os.getenv("OUTPUT_PATH", "outputs")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


def validate_config():
    """
    Call this function at the start of main.py to ensure 
    all critical environment variables and paths are set correctly.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing or empty in your .env file!")
    
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f" Dataset directory not found at: {DATASET_PATH}")
    
    print(" Configuration loaded and validated successfully!")
    print(f"   -> Dataset Path: {DATASET_PATH}")
    print(f"   -> Output Path:  {OUTPUT_PATH}")
    
    
