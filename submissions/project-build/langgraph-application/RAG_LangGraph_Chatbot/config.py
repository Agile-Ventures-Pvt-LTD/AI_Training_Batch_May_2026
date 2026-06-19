import os
from dotenv import load_dotenv

load_dotenv()

# LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Paths
POLICY_DATA_PATH = os.getenv("POLICY_DATA_PATH", "data/policies")
VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "vectorstore")

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))

# Retrieval
TOP_K = int(os.getenv("TOP_K", "4"))


POLICY_DOMAIN_MAP = {
    "hr_leave_policy": "HR_LEAVE",
    "travel_policy": "TRAVEL",
    "reimbursement_policy": "REIMBURSEMENT",
    "it_security_policy": "IT_SECURITY",
    "ai_usage_policy": "AI_USAGE",
}