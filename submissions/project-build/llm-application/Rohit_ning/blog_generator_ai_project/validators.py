import re


SUPPORTED_LENGTHS = ["short", "medium", "long"]


def _is_nonempty_string(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _acceptable_length(value: str) -> bool:
    if not isinstance(value, str):
        return False
    lower = value.strip().lower()
    if lower in SUPPORTED_LENGTHS:
        return True
    return bool(re.search(r"\d+", lower))


def validate_blog_input(payload):
    errors = {}

    topic = payload.get("blog_topic") or payload.get("topic") or ""
    if not _is_nonempty_string(topic):
        errors["blog_topic"] = "Blog topic cannot be empty."

    audience = payload.get("target_audience")
    if not _is_nonempty_string(audience):
        errors["target_audience"] = "Target audience cannot be empty."

    product_context = payload.get("product_or_service_context") or payload.get("product_service_context") or ""
    if not _is_nonempty_string(product_context):
        errors["product_or_service_context"] = "Product / Service context cannot be empty."

    desired_tone = payload.get("desired_tone")
    if not _is_nonempty_string(desired_tone):
        errors["desired_tone"] = "Desired tone cannot be empty."

    key_points = payload.get("key_points") or []
    if not isinstance(key_points, list) or len([p for p in key_points if _is_nonempty_string(p)]) < 3:
        errors["key_points"] = "At least 3 meaningful key points are required."

    blog_length = payload.get("blog_length")
    if not _is_nonempty_string(blog_length) or not _acceptable_length(str(blog_length)):
        errors["blog_length"] = f"Blog length must be one of {SUPPORTED_LENGTHS} or include a word count."

    seo_keywords = payload.get("seo_keywords") or []
    if not isinstance(seo_keywords, list) or len([k for k in seo_keywords if _is_nonempty_string(k)]) < 2:
        errors["seo_keywords"] = "At least 2 SEO keywords are required."

    if not _is_nonempty_string(payload.get("call_to_action") or ""):
        errors["call_to_action"] = "Call to action cannot be empty."

    return len(errors) == 0, errors


def validate_inputs(data: dict):
    """Compatibility wrapper that raises ValueError on invalid input.

    Keeps existing `validate_blog_input` behavior but provides the
    raise-on-error API used in some scripts.
    """
    ok, errors = validate_blog_input(data)
    if not ok:
        # format errors into readable lines
        lines = [f"{k}: {v}" for k, v in errors.items()]
        raise ValueError("\n".join(lines))
    return True


