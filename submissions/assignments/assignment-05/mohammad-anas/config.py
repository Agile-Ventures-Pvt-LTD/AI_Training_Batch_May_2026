import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Please provide API Key")
GROQ_MODEL = os.environ['GROQ_MODEL'] = os.getenv("GROQ_MODEL")
if not GROQ_MODEL:
    print("Please provide groq model")
DB_PATH = os.environ['DB_PATH'] = os.getenv("DB_PATH")
if not DB_PATH:
    print("Please provide db path")