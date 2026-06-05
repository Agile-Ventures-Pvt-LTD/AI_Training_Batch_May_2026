import json
from groq import Groq
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    REQUEST_TIMEOUT
)


class GroqClient:

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not found. "
                "Please configure your .env file."
            )

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,
            min=2,
            max=10
        )
    )
    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 2000
    ) -> str:

        try:

            response = (
                self.client.chat.completions.create(
                    model=GROQ_MODEL,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    timeout=REQUEST_TIMEOUT
                )
            )

            return (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

        except Exception as error:
            raise RuntimeError(
                f"Groq API Error: {error}"
            )


groq_client = GroqClient()