from typing import Any, Dict, List

SUPPORTED_BLOG_LENGTHS = ["short", "medium", "long"]

def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())

def _count_non_empty_items(value: Any) -> int:
    if not isinstance(value, list):
        return 0
    return sum(1 for item in value if isinstance(item, str) and item.strip())

def _is_supported_blog_length(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    raw_value = value.strip().lower()
    return any(length in raw_value for length in SUPPORTED_BLOG_LENGTHS)


def validate_blog_input(user_input: Dict[str, Any]) -> Dict[str, Any]:

    errors: List[str] = []

    if not _is_non_empty_string(user_input.get("blog_topic")):
        errors.append("Blog topic cannot be empty.")

    if not _is_non_empty_string(user_input.get("target_audience")):
        errors.append("Target audience cannot be empty.")

    if _count_non_empty_items(user_input.get("key_points")) < 3:
        errors.append("Please provide at least 3 key points before generating the blog.")

    if not _is_supported_blog_length(user_input.get("blog_length")):
        errors.append(
            f"Blog length must be one of: {', '.join(SUPPORTED_BLOG_LENGTHS)}."
        )

    if _count_non_empty_items(user_input.get("seo_keywords")) < 2:
        errors.append("Please provide at least 2 SEO keywords.")

    if not _is_non_empty_string(user_input.get("call_to_action")):
        errors.append("Call to action cannot be empty.")

    return {
        "valid": not errors,
        "errors": errors,
    }


def get_validation_errors(user_input: Dict[str, Any]) -> List[str]:
    return validate_blog_input(user_input)["errors"]
