from groq import Groq
from config import *

client = Groq(
    api_key=GROQ_API_KEY
)

def call_groq_model(
    prompt,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS
):

    response = client.chat.completions.create(
        model=MODEL_NAME,
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