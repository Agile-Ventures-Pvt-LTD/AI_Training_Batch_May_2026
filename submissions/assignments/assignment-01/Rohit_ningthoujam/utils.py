import json
import re
from pathlib import Path


def extract_json(response_text):

    try:
        return json.loads(response_text)

    except:
        pass

    match = re.search(r"\{.*\}", response_text, re.DOTALL)

    if not match:
        raise ValueError("JSON not found")

    return json.loads(match.group(0))


def save_output(filename, data):

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def run_case(case_name,
             prompt,
             llm_function):

    response = llm_function(prompt)

    parsed = extract_json(response)

    return {
        "case_name": case_name,
        "raw_response": response,
        "parsed_response": parsed
    }