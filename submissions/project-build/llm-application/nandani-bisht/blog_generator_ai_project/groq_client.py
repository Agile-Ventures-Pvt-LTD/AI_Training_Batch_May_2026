from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, DEFAULT_TEMPERATURE

client = None 
MODEL = GROQ_MODEL

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)


def call_groq(prompt, temperature=None):
    """Call Groq chat completion and return the message content."""
    if not client:
        raise ValueError(
            "GROQ_API_KEY is not set. Please create a .env file and set GROQ_API_KEY=your_key_here"
        )
    
    if temperature is None:
        temperature = DEFAULT_TEMPERATURE

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )

    return response.choices[0].message.content

