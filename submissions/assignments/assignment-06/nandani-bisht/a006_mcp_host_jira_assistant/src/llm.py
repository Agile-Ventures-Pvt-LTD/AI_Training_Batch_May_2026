import os
from groq import Groq


class GroqAgent:
    def __init__(self, api_key=None, model=None):
        api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set. Check your .env file.")
        self.model = model or os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
        self._client = Groq(api_key=api_key)

    def next_step(self, messages, tools):
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.1,
        )
        return response.choices[0].message
