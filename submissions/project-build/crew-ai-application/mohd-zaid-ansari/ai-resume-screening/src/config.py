import os
from dotenv import load_dotenv
from crewai import LLM

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL")

DATASET_PATH = os.getenv("DATASET_PATH", "data/p004_resume_screening_crew_dataset")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "outputs")

llm = LLM(
    model=MODEL_NAME,
    api_key=GROQ_API_KEY,
    tool_choice="auto"
)
