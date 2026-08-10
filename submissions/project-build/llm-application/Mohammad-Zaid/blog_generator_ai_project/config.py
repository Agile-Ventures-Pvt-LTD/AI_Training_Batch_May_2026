
import os
from dotenv import load_dotenv

load_dotenv()

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

# Generation Settings
DEFAULT_TEMPERATURE = 0.2

INTENT_MAX_TOKENS = 500
SUMMARY_MAX_TOKENS = 500
OUTLINE_MAX_TOKENS = 500
BLOG_MAX_TOKENS = 2000
SEO_MAX_TOKENS = 500
LINKEDIN_MAX_TOKENS = 500
QUALITY_MAX_TOKENS = 700
HALLUCINATION_MAX_TOKENS = 700

# Output Settings
OUTPUT_FOLDER = "outputs"
OUTPUT_FILE = "sample_blog_output.json"