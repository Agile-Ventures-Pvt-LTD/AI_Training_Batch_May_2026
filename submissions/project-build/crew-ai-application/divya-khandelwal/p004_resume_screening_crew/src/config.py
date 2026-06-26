import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )

    GROQ_MODEL= os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )

    DB_PATH =os.getenv(
        "DB_PATH",
        "data/p004_resume_screening_crew_dataset"
    )

    OUTPUT_PATH= os.getenv(
        "OUTPUT_PATH",
        "outputs"
    )
    
settings = Settings()