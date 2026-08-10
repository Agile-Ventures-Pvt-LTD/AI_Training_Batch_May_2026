import json
import re

def parse_json_safely(text: str) -> dict:
    """Strips markdown code blocks and returns a parsed Python dictionary."""
    try:
        text = text.strip()
        text = re.sub(r'^```json\n?', '', text)
        text = re.sub(r'^```\n?', '', text)
        text = re.sub(r'```$', '', text)
        return json.loads(text.strip())
    except json.JSONDecodeError:
        print("[WARNING] JSON Parse Error. Returning raw output.")
        return {"error": "Failed to parse JSON", "raw_output": text}