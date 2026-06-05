import json
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential

from config import Config


class GroqClient:

    def __init__(self):
        Config.validate()

        self.client = Groq(
            api_key=Config.GROQ_API_KEY
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def call_model(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1500
    ) -> str:

        response = self.client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content.strip()
