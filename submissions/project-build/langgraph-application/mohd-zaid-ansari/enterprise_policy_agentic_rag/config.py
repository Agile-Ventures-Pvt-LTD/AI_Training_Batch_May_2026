from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME =  os.getenv("GROQ_MODEL")

EMBEDDING_MODEL="sentence-transformers/all-mpnet-base-v2" 
POLICY_DATA_PATH="data/policies"
VECTOR_STORE_PATH="vector_store"
CHUNK_SIZE=700
CHUNK_OVERLAP=100  
TOP_K=4

llm = ChatGroq(
    model=MODEL_NAME,  
    groq_api_key=GROQ_API_KEY,
)