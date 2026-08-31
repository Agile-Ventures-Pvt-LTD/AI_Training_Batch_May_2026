from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
import os
from langchain_groq import ChatGroq

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")

DATA_DIR = "data"

KNOWLEDGE_BASE_PATH = "data/logistics_knowledge_base.txt"
INVENTORY_STATUS_PATH = "data/inventory_status.json"
ROUTE_OPTIONS_PATH = "data/route_options.json"
SAMPLE_INCIDENT_PATH = "data/sample_incidents.json"

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 5

MAX_CLARIFICATION_ATTEMPTS=5

FAISS_SAVE_DIR = "faiss_local_index"

# BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = "outputs"

def ensure_output_dir():
    return OUTPUT_DIR

def get_llm():
    llm =  ChatGroq(api_key=API_KEY,model=MODEL_NAME,temperature=0.7,timeout=30)
    return llm