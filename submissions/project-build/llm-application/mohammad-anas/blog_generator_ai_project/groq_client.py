import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import GROQ_API_KEY, GROQ_MODEL

import json
import time
from typing import Any, Dict

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
# from .config import GROQ_API_KEY, GROQ_MODEL

API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
}


class GroqAPIError(RuntimeError):
    pass


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.Timeout, GroqAPIError)),
)
def call_groq(
    messages: list[Dict[str, str]],
    temperature: float = 0.3,
    max_tokens: int = 2000,
) -> str:
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }

    try:
        resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    except requests.Timeout as exc:
        raise GroqAPIError("Request timed out") from exc

    if resp.status_code == 429:
        # rate limit – let tenacity retry after back‑off
        raise GroqAPIError("Rate limit hit")
    if not resp.ok:
        raise GroqAPIError(f"Groq error {resp.status_code}: {resp.text}")

    data = resp.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise GroqAPIError("Malformed response from Groq") from exc
