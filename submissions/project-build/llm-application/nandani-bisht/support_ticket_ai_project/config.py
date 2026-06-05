import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv(dotenv_path=Path('.env'))
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.groq_model = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
        self.default_temperature = float(os.getenv('GROQ_TEMPERATURE', '0.2'))
        self.default_max_tokens = int(os.getenv('GROQ_MAX_TOKENS', '1500'))

        if not self.groq_api_key:
            raise EnvironmentError(
                'Missing GROQ_API_KEY. Add it to .env or your environment before running the app.'
            )


def load_config():
    return Config()
