## setup Groq client
from dotenv import load_dotenv
import os
from groq import Groq
load_dotenv()


def create_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is missing."
        )

    os.environ["GROQ_API_KEY"] = api_key
    return Groq()


try:
    client = create_client()
except Exception as e:
    client = None
    print("Groq client initialization error:", e)