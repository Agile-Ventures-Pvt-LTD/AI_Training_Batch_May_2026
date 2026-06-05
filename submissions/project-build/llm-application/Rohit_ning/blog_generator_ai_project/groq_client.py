from groq import Groq
import os
from tenacity import retry, stop_after_attempt, wait_exponential
from config import GROQ_API_KEY, GROQ_MODEL

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
def call_groq_model(
    prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 2000,
    model: str = None,
):

    model = model or GROQ_MODEL

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


def call_groq_edit(
    input_text,
    instruction,
    model="llama-3.3-70b-versatile",
    temperature=0.2,
):

    response = client.post(
        "/v1/edits",
        body={
            "model": model,
            "input": input_text,
            "instruction": instruction,
            "temperature": temperature,
        },
    )

    return response.choices[0].text


def call_groq_embeddings(
    input_text,
    model="embed-text-3-large",
):

    response = client.embeddings.create(model=model, input=input_text)
    return response.data[0].embedding
