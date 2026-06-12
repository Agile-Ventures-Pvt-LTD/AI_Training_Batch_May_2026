import os
import time

from dotenv import load_dotenv
from groq import Groq, GroqError

from output_parser import parse_json_response

load_dotenv()


def get_env(name: str, default: str = "") -> str:
    value = os.getenv(name, default).strip()
    if not value:
        raise EnvironmentError(
            f"Environment variable '{name}' is required but not set. "
            "Check your .env file or shell environment."
        )
    return value


API_KEY = get_env("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL") or os.getenv("GROQ_MODEL_NAME") or "llama-3.3-70b-versatile"
DEFAULT_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.3"))
DEFAULT_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "2500"))

try:
    client = Groq(api_key=API_KEY)
except GroqError as exc:
    raise RuntimeError(f"Failed to initialise Groq client: {exc}") from exc


def call_llm(messages, temperature: float = DEFAULT_TEMPERATURE, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
    last_error = None

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=60,
            )
            return response.choices[0].message.content
        except GroqError as exc:
            last_error = exc
            time.sleep(2 ** attempt)

    raise RuntimeError(f"Groq API request failed after retries: {last_error}") from last_error


def call_json_llm(messages, temperature: float = DEFAULT_TEMPERATURE, max_tokens: int = DEFAULT_MAX_TOKENS):
    raw_response = call_llm(messages, temperature=temperature, max_tokens=max_tokens)
    try:
        return parse_json_response(raw_response)
    except (ValueError, TypeError) as first_error:
        repair_prompt = [
            {
                "role": "system",
                "content": "You repair model outputs into valid JSON. Return valid JSON only.",
            },
            {
                "role": "user",
                "content": (
                    "Convert this response into valid JSON without adding new information:\n\n"
                    f"{raw_response}"
                ),
            },
        ]
        repaired_response = call_llm(repair_prompt, temperature=0, max_tokens=max_tokens)
        try:
            return parse_json_response(repaired_response)
        except (ValueError, TypeError) as second_error:
            raise ValueError(
                f"Model returned invalid JSON and repair failed. Original error: {first_error}"
            ) from second_error
