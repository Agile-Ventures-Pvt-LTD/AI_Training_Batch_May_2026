import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

def call_groq_model(prompt: str, system_prompt: str = "", temperature: float = 0.3, max_tokens: int = 2000) -> str:
    """
    Calls Groq API and returns the model response as text. Includes basic retry logic for rate limits.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_str = str(e).lower()
            if "rate limit" in error_str or "429" in error_str:
                wait_time = (attempt + 1) * 3
                print(f"[API WARN] Rate limit hit. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"[API ERROR] Model failure: {e}")
                if attempt == max_retries - 1:
                    return '{"error": "API failed after retries"}'
    return '{"error": "Max retries reached"}'