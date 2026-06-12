import json
import re
from datetime import datetime


def extract_json(response_text):
    """
    Extract JSON even if LLM adds extra text.
    """
    try:
        return json.loads(response_text)
    except:
        pass

    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None

    match = re.search(r"\[.*\]", response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None

    return None


def save_output(filename, data):

    import os
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return path


def run_case(case_name, prompt, llm_fn, temperature=0.2):
    raw = llm_fn(prompt, temperature=temperature)
    parsed = extract_json(raw)

    return {
        "case_name": case_name,
        "raw_output": raw,
        "parsed": parsed,
        "timestamp": str(datetime.now())
    }
    return result
