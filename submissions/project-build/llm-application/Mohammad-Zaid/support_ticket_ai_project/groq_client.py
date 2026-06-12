from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, DEFAULT_TEMPERATURE

client = Groq(api_key=GROQ_API_KEY)


def call_groq_model(system_prompt, user_prompt, temperature=DEFAULT_TEMPERATURE, max_tokens=1000
):
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(
            f"Groq API Error: {str(e)}"
        )