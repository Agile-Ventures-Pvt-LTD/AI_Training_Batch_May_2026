import json
import os
import re
from groq_client import call_llm


def extract_json(text):
    """
    Extract JSON object from model response.
    """

    try:
        return json.loads(text)
    except:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except Exception as e:
            print("JSON parsing failed:", e)

    return None


def save_output(filename, data):
    os.makedirs("outputs", exist_ok=True)

    path = os.path.join("outputs", filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved -> {path}")


def run_case(case_name, prompt_messages, output_filename, temperature=0.2):
    print(f"\nRunning: {case_name}")

    response = call_llm(
        messages=prompt_messages,
        temperature=temperature
    )

    parsed = extract_json(response)

    result = {
        "case_name": case_name,
        "raw_response": response,
        "parsed_output": parsed
    }

    save_output(output_filename, result)

    return result