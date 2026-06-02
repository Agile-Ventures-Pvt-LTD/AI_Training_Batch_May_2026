
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

DEFAULT_MODEL = "llama-3.3-70b-versatile"


def call_llm(
    prompt,
    temperature=0.2,
    model=DEFAULT_MODEL,
    max_tokens=2000
):

    

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

