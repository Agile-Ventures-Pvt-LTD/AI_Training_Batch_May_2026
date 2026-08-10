import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

DATASET_PATH = os.getenv("DATASET_PATH","data")
OUTPUT_PATH = os.getenv("OUTPUT_PATH","outputs")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")




class GroqLLM:
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
            max_retries=0  
        )
        self.model = "llama-3.1-8b-instant"  

    def bind(self, **kwargs):
        return self

    def invoke(self, prompt):
        if isinstance(prompt, dict):
            prompt = json.dumps(prompt)
        elif isinstance(prompt, list):
            prompt = "\n".join([str(p) for p in prompt])
        else:
            prompt = str(prompt)

        prompt = prompt[:2000]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            print("LLM failed (rate limit or API issue):", str(e))
            return "Fallback response due to API limit."

    def __call__(self, prompt):
        return self.invoke(prompt)


def get_llm():
    return GroqLLM()