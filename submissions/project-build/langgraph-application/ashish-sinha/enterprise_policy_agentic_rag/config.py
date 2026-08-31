import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

# os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 900))

CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 120))

TOP_K = int( os.getenv("TOP_K", 4))

VECTOR_STORE_PATH = "vector_store"

POLICY_DATA_PATH = os.getenv("POLICY_DATA_PATH","data/policies")

MAX_REWRITE_RETRIES = 1

# POLICY_DOMAINS = ["HR_LEAVE","TRAVEL","REIMBURSEMENT","IT_SECURITY","AI_USAGE"]

# POLICY_FILES = {
#     "HR_LEAVE": "hr_leave_policy.md",
#     "TRAVEL": "travel_policy.md",
#     "REIMBURSEMENT": "reimbursement_policy.md",
#     "IT_SECURITY": "it_security_policy.md",
#     "AI_USAGE": "ai_usage_policy.md"
# }

llm = ChatGroq(model=GROQ_MODEL,api_key=GROQ_API_KEY,temperature=0)