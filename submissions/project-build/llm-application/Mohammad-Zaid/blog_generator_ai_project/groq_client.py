import os
from groq import Groq
from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    DEFAULT_TEMPERATURE
)

# Validate API Key 
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing.")

# Create Groq client once
client = Groq(api_key=GROQ_API_KEY)

def call_groq_model(system_prompt, user_prompt, temperature=DEFAULT_TEMPERATURE, max_tokens=500):
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content
