import os
import json
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
from prompts import user_message_template

load_dotenv()  

MODEL_NAME = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def run_case(messages, temperature=0.2, max_tokens=1500):
    """
    Send messages to the model and return the raw response string.
    Raises a clear error if the API key is missing.
    """
    if not os.environ.get("GROQ_API_KEY"):
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Please add it to your .env file."
        )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Groq API call failed: {e}") from e


def build_prompt(system_msg, question, context=None):
    user_msg = user_message_template.format(question=question, context=context) if context else question
    messages = [{"role": "system", "content": system_msg}]
    messages.append({"role": "user", "content": user_msg})
    return messages