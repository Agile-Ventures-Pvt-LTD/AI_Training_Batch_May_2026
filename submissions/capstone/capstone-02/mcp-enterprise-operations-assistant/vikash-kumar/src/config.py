import os
from dotenv import load_dotenv

load_dotenv()

class Mcp:        
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("Groq api not not found")
