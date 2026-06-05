from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def call_groq_model(prompt: str, temperature: float = 0.2, max_tokens: int = 1000) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=60.0,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Groq API error: {str(e)}")
