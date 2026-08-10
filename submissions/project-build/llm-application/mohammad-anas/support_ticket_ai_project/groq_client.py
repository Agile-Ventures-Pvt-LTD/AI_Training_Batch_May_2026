import time
from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME


if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Please set it in your .env file.")

client = Groq(api_key=GROQ_API_KEY)

def call_groq_model(prompt: str, system_prompt: str = "", temperature: float = 0.2, max_tokens: int = 1500) -> str:
    """Calls Groq API with robust error handling and exponential backoff."""
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
                print(f"[API WARN] Rate limit or timeout. Retrying")
                time.sleep(wait_time)
            else:
                print(f"[API ERROR] Model failure: {e}")
                if attempt == max_retries - 1:
                    return '{"error": "API failed after max retries."}'
    return '{"error": "Max retries reached."}'