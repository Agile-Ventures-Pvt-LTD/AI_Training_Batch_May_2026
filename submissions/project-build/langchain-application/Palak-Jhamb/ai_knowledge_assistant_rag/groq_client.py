import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqClient:

    def __init__(self, model="openai/gpt-oss-120b"):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = model

    def generate(self, system_prompt, user_prompt):

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            # response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return response.choices[0].message.content