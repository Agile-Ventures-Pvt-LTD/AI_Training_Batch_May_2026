from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(
    api_key = os.environ.get("GROQ_API_KEY")

)

def call_llm(prompt, model = "llama-3.3-70b-versatile", temperature=0.2):
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content