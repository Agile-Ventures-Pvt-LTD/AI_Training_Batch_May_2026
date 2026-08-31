import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
from tenacity import retry,stop_after_attempt,wait_exponential

# Initialize Groq Client

client = Groq()

@retry(stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1))

# LLM Call Function

def call_groq_model(
    prompt: str,
    model: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    temperature: float = 0.3,
    max_tokens: int = 5000,
) -> str:
    """
    Call Groq LLM and return text response.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content



