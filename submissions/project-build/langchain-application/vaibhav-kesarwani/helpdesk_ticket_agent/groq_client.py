import os
from dotenv import load_dotenv
from groq import Groq, RateLimitError, APIConnectionError, APIStatusError

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")

client = Groq(api_key=os.environ["GROQ_API_KEY"])
model_name = "openai/gpt-oss-120b"

def call_groq(prompt: list, temperature: float = 0.2):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=prompt,
            temperature=temperature
        )

        return response.choices[0].message.content.strip()

    except RateLimitError:
        print("Rate limit exceeded.")
    except APIConnectionError:
        print("Failed to connect to Groq API.")
    except APIStatusError as e:
        print(f"Groq API returned an error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None