from groq import Groq
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

if not GROQ_API_KEY:
    raise ValueError(
        "Missing GROQ_API_KEY"
    )

client = Groq(
    api_key=GROQ_API_KEY
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1)
)
def call_groq_model(
    prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 2000
):

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content


