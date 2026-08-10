from groq import Groq

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)



client = Groq(api_key="GROQ_API_KEY")



def call_groq_model(
    prompt: str,
    temperature: float = TEMPERATURE,
    max_tokens: int = MAX_TOKENS
):

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
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