
import json
import re


def parse_json(text: str):
    if not text:
        return None

    text = text.strip()
    # remove fenced code blocks if present
    text = text.replace("```json", "")
    text = text.replace("```", "")

    # find first JSON object or array
    match = re.search(r"(\{(?:.|\n)*\}|\[(?:.|\n)*\])", text, re.DOTALL)

    if not match:
        raise ValueError(f"No JSON found.\nRaw output:\n{text}")

    return json.loads(match.group())


def ensure_dict(value):
    if isinstance(value, dict):
        return value
    return {}
