import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="guardrails")

import os
from guardrails import Guard
from guardrails.hub import ProfanityFree
from groq import Groq

client = Groq()

def llm_wrapper(messages=None, model=None, **kwargs):
    return client.chat.completions.create(model=model, messages=messages, **kwargs).choices[0].message.content

class SafetyGuardrails:
    def __init__(self):
        self.guard = Guard().use(ProfanityFree(on_fail="fix"))
        self.model_name = "llama-3.3-70b-versatile"

    def clean_query(self, user_query: str) -> str:
        messages = [{"role": "user", "content": user_query}]
        validated_output = self.guard(llm_wrapper,messages=messages,model=self.model_name)
        return str(validated_output.validated_output)
