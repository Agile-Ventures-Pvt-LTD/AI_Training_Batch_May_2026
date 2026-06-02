from groq import Groq
from dotenv import load_dotenv
import os

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

# =========================================================
# CREATE GROQ CLIENT
# =========================================================
api_key = os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    raise EnvironmentError(
        "Missing API key. Set GROQ_API_KEY or GEMINI_API_KEY in .env or the environment."
    )

client = Groq(
    api_key=api_key
)

# =========================================================
# FUNCTION TO CALL LLM
# =========================================================

def call_llm(
    prompt,
    model=    "gemini-1.5-flash",
    temperature=0.2
):

    try:

        response = client.chat.completions.create(

            model=model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant that returns "
                        "structured and accurate responses."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=temperature,

            max_tokens=2000
        )

        return response.choices[0].message.content

    except Exception as e:

        print("\nLLM API Error:")
        print(e)

        return None