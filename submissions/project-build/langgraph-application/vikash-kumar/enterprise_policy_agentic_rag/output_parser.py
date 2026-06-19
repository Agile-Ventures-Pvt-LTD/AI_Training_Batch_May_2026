import json
import re

def safe_json_parse(text: str):
    if not text:
        return {}
    try:
        return json.loads(text)
    except Exception as e:
        print("the error occured {e}")
    try:
        cleaned = (text.replace("```json", "").replace("```", "").strip())
        return json.loads(cleaned)

    except Exception:
        pass

    return {}