import json
import re
import logging
from typing import Any, Dict
logger = logging.getLogger(__name__)


def parse_json_response(raw: str, context_label: str = "") -> Dict[str, Any]:
    if not raw or not raw.strip():
        logger.warning("Empty response received for: %s", context_label)
        return {}

    text = raw.strip()

    fence_match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
    if fence_match:
        text = fence_match.group(1).strip()

    brace_match = re.search(r"\{[\s\S]+\}", text)
    if brace_match:
        text = brace_match.group(0)

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error("JSON parse failed for %s: %s | Raw: %.200s", context_label, str(e), raw)
        return {}


def safe_str(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    return str(value).strip()


def safe_list(value: Any) -> list:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]




