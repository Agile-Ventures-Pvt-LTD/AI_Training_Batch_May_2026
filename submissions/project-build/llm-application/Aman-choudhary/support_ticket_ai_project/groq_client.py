import json
from groq import Groq
from tenacity import (retry,stop_after_attempt,wait_exponential)
from config import (GROQ_API_KEY,GROQ_MODEL,TEMPERATURE,MAX_TOKENS)
client = Groq(api_key=GROQ_API_KEY)
@retry(stop=stop_after_attempt(3),wait=wait_exponential(multiplier=1,min=2,max=10))
def call_groq(prompt: str,temperature: float = TEMPERATURE,max_tokens: int = MAX_TOKENS):
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content