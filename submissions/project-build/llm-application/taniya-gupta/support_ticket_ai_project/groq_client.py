import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY=os.getenv('GROQ_API_KEY')
MODEL= os.getenv('GROQ_MODEL')
client = Groq()

def call_groq_model(prompt: str, temperature: float = 0.3, max_tokens: int = 2000) -> str:
    message = client.chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.choices[0].message.content