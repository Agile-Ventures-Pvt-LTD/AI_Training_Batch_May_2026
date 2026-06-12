import json
import re
from datetime import datetime


def extract_json(response):
    """
    Extract JSON even if LLM adds extra text.
    """
    try:
        return json.loads(response)
    except:
        pass

    match = re.search(r"\{.*\}", response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None

    match = re.search(r"\[.*\]", response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None

    return None


def save_output(filename, data):

    import os
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return path


def run_case(case_name, prompt, llm_fn, temperature=0.2):
    raw = llm_fn(prompt, temperature=temperature)
    parsed = extract_json(raw)

    return {
        
 "title": "",
 "outline": [
 {
 "section_heading": "",
 "section_purpose": "",
 "key_points_to_cover": []
 }
 ],
 "cta_placement": "",
 "estimated_word_count": 0
        
}
    return result
