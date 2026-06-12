import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    try:
        os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    except Exception as e:
        print(f"Missing groq api key: {e}")