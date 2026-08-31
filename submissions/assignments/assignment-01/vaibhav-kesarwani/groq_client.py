from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_llm(messages, model_name="llama-3.3-70b-versatile", temperature=0.2):
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature
    )

    return response.choices[0].message.content