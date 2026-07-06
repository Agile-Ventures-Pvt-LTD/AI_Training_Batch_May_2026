import os

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
