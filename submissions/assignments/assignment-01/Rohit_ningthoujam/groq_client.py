from groq import Groq
import os
import json
import re

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def call_llm(
    prompt,
    model="llama-3.3-70b-versatile",
    temperature=0.2
):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content


def extract_json(response_text):

    if not response_text:
        return None

    try:
        return json.loads(response_text)
    except:
        pass

    try:
        array_match = re.search(
            r"\[.*\]",
            response_text,
            re.DOTALL
        )

        if array_match:
            return json.loads(array_match.group())
    except:
        pass

    try:
        object_match = re.search(
            r"\{.*\}",
            response_text,
            re.DOTALL
        )

        if object_match:
            return json.loads(object_match.group())
    except:
        pass

    return None


def save_output(filename, data):

    os.makedirs("outputs", exist_ok=True)

    filepath = os.path.join("outputs", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    return filepath


def run_case(
    case_name,
    prompt,
    temperature=0.2
):

    raw_response = call_llm(
        prompt,
        temperature=temperature
    )

    parsed_response = extract_json(raw_response)

    if parsed_response is None:

        parsed_response = {
            "error": "Invalid JSON returned by model",
            "raw_response": raw_response
        }

    return parsed_response