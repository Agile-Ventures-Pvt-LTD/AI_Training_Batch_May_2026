import json
import re

def parse_json(text: str):

    text = text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(
            f"No JSON found.\nRaw output:\n{text}"
        )

    return json.loads(match.group())
    