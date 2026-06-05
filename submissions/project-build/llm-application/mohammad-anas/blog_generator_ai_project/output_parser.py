import json
import re

def parse_json_safely(text: str) -> dict:
    """Strips markdown formatting and parses JSON safely."""
    try:
        # Remove markdown code blocks if present
        text = re.sub(r'```json\n?', '', text)
        text = re.sub(r'```\n?', '', text)
        return json.loads(text.strip())
    except json.JSONDecodeError:
        print("[WARNING] Failed to parse JSON. Returning raw string inside dict.")
        return {"raw_output": text}