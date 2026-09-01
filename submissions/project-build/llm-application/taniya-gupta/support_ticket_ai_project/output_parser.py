import ast
import json
import re
from datetime import datetime

def _clean_json_like_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json|text)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    text = text.replace("'", '"')
    text = re.sub(r"\n\s+", " ", text)
    text = re.sub(r",\s*([}\]])", r"\1", text)
    text = re.sub(r"([\{\[\s,])([A-Za-z0-9_]+)\s*:", r"\1\"\2\":", text)
    text = re.sub(r"\bNone\b", "null", text)
    text = re.sub(r"\bTrue\b", "true", text)
    text = re.sub(r"\bFalse\b", "false", text)
    text = re.sub(r"^\s*['\"]?\s+", "", text)
    text = re.sub(r"\s+['\"]?\s*$", "", text)
    return text


def _parse_key_value_pairs(text: str):
    data = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip().strip('"\'')
        if not key or not re.match(r"^[A-Za-z0-9_]+$", key):
            continue

        value = value.strip()
        if not value:
            continue

        if value.startswith(("\"", "'")) and value.endswith(("\"", "'")):
            value = value[1:-1]
        else:
            try:
                value = json.loads(value)
            except Exception:
                try:
                    value = ast.literal_eval(value)
                except Exception:
                    pass

        data[key] = value
    return data


def parse_json(text):
    if isinstance(text, (dict, list)):
        return text

    if text is None:
        return {}

    if not isinstance(text, str):
        text = str(text)

    text = text.strip()
    if not text:
        return {}

    try:
        result = json.loads(text)
        return result
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        candidate = match.group(0)
        cleaned = _clean_json_like_text(candidate)
        try:
            result = json.loads(cleaned)
            return result
        except Exception:
            pass
        try:
            result = ast.literal_eval(cleaned)
            return result
        except Exception:
            pass

    cleaned = _clean_json_like_text(text)

    try:
        result = json.loads(cleaned)
        return result
    except Exception:
        pass

    try:
        result = ast.literal_eval(cleaned)
        return result
    except Exception:
        pass

    kv_result = _parse_key_value_pairs(text)
    if kv_result:
        return kv_result


