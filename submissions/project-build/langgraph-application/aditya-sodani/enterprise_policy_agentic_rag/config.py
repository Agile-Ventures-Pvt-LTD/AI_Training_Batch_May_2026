import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY","")
GROQ_MODEL = os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")
POLICY_DATA_PATH = os.getenv("POLICY_DATA_PATH","data/policies")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH","vector_store")
OUTPUT_PATH = os.getenv("OUTPUT_PATH","outputs")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE",900))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP",120))
TOP_K = int(os.getenv("TOP_K",4))
MAX_RETRY_COUNT = int(os.getenv("MAX_RETRY_COUNT",1))
POLICY_MAPPING = {"hr_leave_policy": "HR_LEAVE","travel_policy": "TRAVEL",
    "reimbursement_policy": "REIMBURSEMENT","it_security_policy": "IT_SECURITY","ai_usage_policy": "AI_USAGE"}

VALID_QUERY_TYPES = ["HR_LEAVE","TRAVEL","REIMBURSEMENT","IT_SECURITY","AI_USAGE","MULTI_POLICY","AMBIGUOUS","OTHER","UNANSWERABLE"]
SUPPORTED_EXTENSIONS = [".md",".txt",".pdf"]

APP_NAME = ("Enterprise Policy Assistant")

VERSION = "1.0.0"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"