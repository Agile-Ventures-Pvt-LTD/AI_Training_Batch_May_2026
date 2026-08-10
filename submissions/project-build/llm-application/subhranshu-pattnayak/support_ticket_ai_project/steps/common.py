import json
from typing import Any

from groq_client import call_json_llm
from output_parser import require_keys, require_object


def as_json_text(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False)


def format_prompt(prompt: str, **values: Any) -> list[dict[str, str]]:
    return [{"role": "user", "content": prompt.format(**_prepare(values))}]


def format_messages(messages: list[dict[str, str]], **values: Any) -> list[dict[str, str]]:
    prepared = _prepare(values)
    return [{**message, "content": message["content"].format(**prepared)} for message in messages]


def checked_llm_json(
    messages: list[dict[str, str]],
    required_keys: list[str],
    label: str,
    max_tokens: int = 1000,
) -> dict[str, Any]:
    response = call_json_llm(messages, max_tokens=max_tokens)
    response = require_object(response, label)
    require_keys(response, required_keys, label)
    return response


def _prepare(values: dict[str, Any]) -> dict[str, str]:
    return {
        key: as_json_text(value) if isinstance(value, (dict, list)) else str(value)
        for key, value in values.items()
    }
