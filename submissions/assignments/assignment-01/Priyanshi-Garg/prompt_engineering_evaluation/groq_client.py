from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def call_llm(system_prompt, user_input, model, temperature):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content

print(call_llm.__code__.co_varnames)