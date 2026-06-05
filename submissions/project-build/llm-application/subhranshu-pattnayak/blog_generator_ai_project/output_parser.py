import json
import re


def extract_json_text(text: str) -> str:
    text = text.strip()
    fenced_match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fenced_match:
        text = fenced_match.group(1).strip()

    start_candidates = [index for index in [text.find("{"), text.find("[")] if index != -1]
    if not start_candidates:
        raise ValueError("Model response did not contain JSON.")

    start = min(start_candidates)
    end = max(text.rfind("}"), text.rfind("]"))
    if end == -1 or end < start:
        raise ValueError("Model response JSON was incomplete.")

    return text[start : end + 1]


def parse_json_response(text: str):
    return json.loads(extract_json_text(text))
