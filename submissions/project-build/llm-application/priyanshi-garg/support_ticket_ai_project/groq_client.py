from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()


try:

    def get_groq_client(system_prompt, user_input, model, temperature):
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content

except Exception as e:
    print(f"Missing API key: {e}")