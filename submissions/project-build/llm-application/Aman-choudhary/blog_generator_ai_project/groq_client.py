from groq import Groq
from tenacity import (retry,stop_after_attempt,wait_exponential)
from config import (GROQ_API_KEY,GROQ_MODEL)

client = Groq(    
              api_key=GROQ_API_KEY
)
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1)
)

def call_groq_model(
    prompt,
    temperature=0, 
    max_tokens=2000 
):

    response = client.chat.completions.create(
        model=GROQ_MODEL,
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
