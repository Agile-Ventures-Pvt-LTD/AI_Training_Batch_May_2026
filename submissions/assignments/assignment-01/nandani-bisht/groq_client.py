from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def call_llm(prompt, model="llama-3.3-70b-versatile", temperature=0.2):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message.content


def extract_json(response_text):
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", response_text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    decoder = json.JSONDecoder()
    results = []
    text = response_text
    for i, ch in enumerate(text):
        if ch not in "{[":
            continue
        try:
            obj, _ = decoder.raw_decode(text, i)
            if obj not in results:
                results.append(obj)
        except json.JSONDecodeError:
            continue

    if len(results) == 1:
        return results[0]
    if len(results) > 1:
        return results

    raise ValueError("No valid JSON found in response")


def save_output(filename, data):
    with open(f"outputs/{filename}", "w") as f:
        json.dump(data, f, indent=2)


def run_case(case_name, prompt, temperature=0.2):
    response = call_llm(prompt, temperature=temperature)
    try:
        result = extract_json(response)
    except (ValueError, json.JSONDecodeError):
        print("Raw model response:\n", response)
        raise
    save_output(f"{case_name}.json", result)
    return result
