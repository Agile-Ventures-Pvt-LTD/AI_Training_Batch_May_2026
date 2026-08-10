import json
import re
from typing import Any


JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def _extract_json_text(raw_response: str) -> str:
    if not isinstance(raw_response, str) or not raw_response.strip():
        raise ValueError("LLM response is empty.")

    text = raw_response.strip()
    fenced_match = JSON_BLOCK_RE.search(text)
    if fenced_match:
        return fenced_match.group(1).strip()

    first_object = text.find("{")
    last_object = text.rfind("}")
    first_array = text.find("[")
    last_array = text.rfind("]")

    object_candidate = ""
    if first_object != -1 and last_object > first_object:
        object_candidate = text[first_object : last_object + 1]

    array_candidate = ""
    if first_array != -1 and last_array > first_array:
        array_candidate = text[first_array : last_array + 1]

    if object_candidate and array_candidate:
        return object_candidate if first_object < first_array else array_candidate
    if object_candidate:
        return object_candidate
    if array_candidate:
        return array_candidate

    return text


def parse_json_response(raw_response: str) -> Any:
    json_text = _extract_json_text(raw_response)
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Unable to parse LLM response as JSON: {exc}") from exc


def require_object(value: Any, label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object.")
    return value


def require_keys(value: dict, required_keys: list[str], label: str) -> dict:
    missing = [key for key in required_keys if key not in value]
    if missing:
        raise ValueError(f"{label} is missing required keys: {', '.join(missing)}.")
    return value