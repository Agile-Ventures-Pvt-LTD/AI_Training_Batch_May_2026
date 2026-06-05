#import prompts

# Ticket Summarization



def call_groq_model(prompt:str, temperature:float=0.7, max_tokens:int=1500) -> str:
    response = client.chat.completions(
        model=GROQ_MODEL,
        messages=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

