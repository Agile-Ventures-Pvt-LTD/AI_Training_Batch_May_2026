import os
import json
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"


def run_case(messages, temperature=0.2):
    """
    Send messages to the model and return the raw response string.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content


def build_prompt(system_msg, user_msg, examples=None):
    messages = [{"role": "system", "content": system_msg}]
    if examples:
        for ex in examples:
            messages.append({"role": ex["role"], "content": ex["content"]})
    messages.append({"role": "user", "content": user_msg})
    return messages


OUTPUT_DIR = Path("outputs")

def save_output(name: str, raw: str):
    clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
    path = OUTPUT_DIR / f"{name}.json"
    with open(path, "w") as f:
        f.write(clean)
    print(f"  -> saved to {path}")

