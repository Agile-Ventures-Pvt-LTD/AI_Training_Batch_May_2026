import requests
from requests.exceptions import RequestException, Timeout
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import load_config


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(RequestException),
)
def call_groq_model(
    prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 1500,
    timeout: int = 30,
) -> str:
    config = load_config()

    headers = {
        "Authorization": f"Bearer {config.groq_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": config.groq_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=timeout,
        )
    except Timeout as exc:
        raise RequestException("Groq API request timed out.") from exc

    if response.status_code == 401:
        raise EnvironmentError(
            "Groq API authentication failed. Check GROQ_API_KEY."
        )

    if response.status_code == 429:
        raise RequestException("Groq API rate limit exceeded.")

    if response.status_code >= 500:
        raise RequestException(
            f"Groq API service error: {response.status_code}"
        )

    response.raise_for_status()

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        raise ValueError("Unexpected Groq API response format.")