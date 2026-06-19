import json
import re

def clean_json(text):
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if match:
        return match.group(1).strip()
    return text.strip()

def parse_json(text):
    cleaned=clean_json(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start=cleaned.find('{')
        end=cleaned.rfind('}')
        if start!=-1 and end!=-1:
            return json.loads(cleaned[start:end+1])