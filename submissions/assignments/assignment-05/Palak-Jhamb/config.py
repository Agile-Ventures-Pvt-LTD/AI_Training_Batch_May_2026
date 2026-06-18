DB_PATH='data/ccms.db'

import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    try:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("API key not found")
        return key

    except Exception as e:
        print(f"API KEY not found: {e}")
        return None