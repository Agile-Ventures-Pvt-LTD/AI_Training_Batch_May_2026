import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )

    TEMPERATURE_CLASSIFICATION = 0.1
    TEMPERATURE_ANALYSIS = 0.2
    TEMPERATURE_RESPONSE = 0.4

    MAX_TOKENS = 1500

    OUTPUT_DIR = "outputs"

    @staticmethod
    def validate():
        if not Config.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not found. Please configure your .env file."
            )



