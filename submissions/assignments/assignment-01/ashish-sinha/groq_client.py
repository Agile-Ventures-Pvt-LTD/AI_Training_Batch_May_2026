import os
from groq import Groq


# Initialize Groq Client

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


# LLM Call Function

def call_llm(
    prompt: str,
    model: str = "openai/gpt-oss-120b",
    temperature: float = 0.2,
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
