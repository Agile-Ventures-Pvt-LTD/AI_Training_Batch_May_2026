import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv( "GROQ_MODEL","llama-3.3-70b-versatile")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

MAX_CLARIFICATION_ATTEMPTS = 2

LOGISTICS_KB_PATH = DATA_DIR / "logistics_knowledge_base.txt"
INVENTORY_STATUS_PATH = DATA_DIR / "inventory_status.json"
ROUTE_OPTIONS_PATH = DATA_DIR / "route_options.json"
SAMPLE_INCIDENTS_PATH = DATA_DIR / "sample_incidents.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)