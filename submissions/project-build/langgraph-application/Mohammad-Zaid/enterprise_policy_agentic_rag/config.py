"""
Configuration settings for the Enterprise Policy Agentic RAG system.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLM Configuration
LLM_MODEL = "llama-3.1-8b-instant"
LLM_TEMPERATURE = 0.0
LLM_MAX_RETRIES = 2
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Vector Store Configuration
VECTOR_STORE_PATH = "./vector_store"
COLLECTION_NAME = "policy-chunks"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Document Processing Configuration
POLICIES_FOLDER = "./data/policies"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
SEARCH_K = 3  # Number of documents to retrieve

# Metadata keys
METADATA_SOURCE_FILE = "source_file"
METADATA_POLICY_DOMAIN = "policy_domain"
METADATA_PAGE_NUMBER = "page_number"
METADATA_CHUNK_ID = "chunk_id"
