import os
import json
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

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


def build_prompt(system_msg, user_msg, examples=None):
    """
    Build a messages list for the Groq API.
    Pass few-shot examples as a list of {"role": ..., "content": ...} dicts.
    """
    messages = [{"role": "system", "content": system_msg}]
    if examples:
        for ex in examples:
            messages.append({"role": ex["role"], "content": ex["content"]})
    messages.append({"role": "user", "content": user_msg})
    return messages


def parse_json_response(raw: str) -> dict:
    """
    Strip markdown fences and parse the model's JSON response.
    Raises ValueError with a clear message if parsing fails.
    """
    clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model returned invalid JSON: {e}\nRaw output:\n{raw}") from e


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def save_output(name: str, raw: str):
    """
    Strip markdown fences, write clean JSON to outputs/<name>.json.
    """
    clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    path = OUTPUT_DIR / f"{name}.json"
    with open(path, "w") as f:
        f.write(clean)
    print(f"  -> saved to {path}")
