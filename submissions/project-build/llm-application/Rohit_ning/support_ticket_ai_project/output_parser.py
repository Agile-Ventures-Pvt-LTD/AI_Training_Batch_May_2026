import json
import re


def parse_json(text: str) -> dict:

    text = text.strip()
    text = re.sub(r"```json\s*\n?", "", text)
    text = re.sub(r"```\s*\n?", "", text)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Unable to parse model output as JSON.\nRaw output:\n{text}")
