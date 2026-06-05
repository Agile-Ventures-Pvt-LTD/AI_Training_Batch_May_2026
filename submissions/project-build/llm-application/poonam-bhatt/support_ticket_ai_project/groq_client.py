from groq import Groq
import os
import json
from dotenv import load_dotenv
load_dotenv()



client = Groq(
    api_key=os.getenv("GROQ_API_KEY")  
)

print("Groq connected")



def call_groq(prompt, model="openai/gpt-oss-120b", temperature=0):
    

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict enterprise AI system. "
                        "Return ONLY valid JSON. No explanations."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            response_format={"type": "json_object"}
        )

        return response.choices[0].message.content

    except Exception as e:
        return json.dumps({
            "error": "Groq API call failed",
            "details": str(e)
        })




import json
import os
from datetime import datetime

def parse_json_safe(data, folder="outputs"):
    """
    Saves final ticket output as JSON file
    """

    # create folder if not exists
    os.makedirs(folder, exist_ok=True)

    # unique filename using timestamp
    filename = f"{folder}/ticket_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return filename