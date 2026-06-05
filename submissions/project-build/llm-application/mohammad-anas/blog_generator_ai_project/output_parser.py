import json
from typing import List, Dict

def safe_json_parse(text: str) -> Dict[str, any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.find("}") + 1
        if start == -1 or end == -1:
            raise ValueError("No JSON obect found")
        try:
            return json.load(text[start:end])
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to parse JSON from LLM") from exc
    
    