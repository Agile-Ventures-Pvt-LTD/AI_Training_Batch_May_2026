import os 
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
GROQ_MODEL=os.getenv("GROQ_MODEL")
DATASET_PATH=os.getenv("DATASET_PATH")
OUTPUT_PATH=os.getenv("OUTPUT_PATH")

os.makedirs(OUTPUT_PATH, exist_ok=True)