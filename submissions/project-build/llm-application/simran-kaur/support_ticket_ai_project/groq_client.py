
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

DEFAULT_MODEL = "openai/gpt-oss-120b"

"""
def call_llm(
    system_prompt,
    user_prompt,
    temperature=0.2,
    model=DEFAULT_MODEL,
    max_tokens=2000
):

    
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
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
    except Exception as e:
        print(e)

    return response.choices[0].message.content

    """

def call_llm(
    prompt,
    temperature=0.2,
    model=DEFAULT_MODEL,
    max_tokens=2000
):

    
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=prompt
        )
    except Exception as e:
        print(e)

    return response.choices[0].message.content

