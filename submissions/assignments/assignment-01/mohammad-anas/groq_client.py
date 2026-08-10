import os
from groq import Groq
from dotenv import load_dotenv

# Loading Environmental varaible from .env
load_dotenv()

# get api key
api_key = os.getenv("GROQ_API_KEY")

#create groq client
client = Groq(api_key=api_key)

def call_llm(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5
    )
    return response.choices[0].message.content