def validate_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()


def validate_length(value: str, field_name: str, max_len: int = 200) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be text.")
    if len(value) > max_len:
        raise ValueError(f"{field_name} exceeds {max_len} characters.")
    return value


def validate_tone(value: str) -> str:
    return validate_non_empty(value, "Desired tone")


def validate_key_points(value) -> list:
    if isinstance(value, str):
        points = [point.strip(" -\t") for point in value.splitlines() if point.strip()]
    elif isinstance(value, list):
        points = [str(point).strip() for point in value if str(point).strip()]
    else:
        points = []

    meaningful_points = [point for point in points if len(point.split()) >= 3]
    if len(meaningful_points) < 3:
        raise ValueError("Please provide at least 3 meaningful key points before generating the blog.")
    return points


def validate_blog_length(value: str) -> str:
    value = validate_non_empty(value, "Blog length")
    normalized = value.lower()
    supported_lengths = ["short", "medium", "long"]
    includes_supported_label = any(length in normalized for length in supported_lengths)
    includes_word_count = any(char.isdigit() for char in normalized)

    if not includes_supported_label and not includes_word_count:
        raise ValueError("Blog length must be short, medium, long, or include an approximate word count.")
    return value


def validate_keywords(value) -> list:
    if isinstance(value, str):
        keywords = [keyword.strip() for keyword in value.split(",") if keyword.strip()]
    elif isinstance(value, list):
        keywords = [str(keyword).strip() for keyword in value if str(keyword).strip()]
    else:
        keywords = []

    if len(keywords) < 2:
        raise ValueError("Please provide at least 2 SEO keywords.")
    return keywords


def validate_optional_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip(" -\t") for item in value.splitlines() if item.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def validate_inputs(inputs: dict) -> dict:
    if not isinstance(inputs, dict):
        raise ValueError("Inputs must be provided as a dictionary.")

    product_context = validate_length(
        inputs.get("product_or_service_context", ""),
        "Product / Service Context",
        1000,
    )

    return {
        "blog_topic": validate_non_empty(inputs.get("blog_topic"), "Blog topic"),
        "target_audience": validate_non_empty(inputs.get("target_audience"), "Target audience"),
        "product_or_service_context": validate_non_empty(product_context, "Product / Service Context"),
        "key_points": validate_key_points(inputs.get("key_points")),
        "desired_tone": validate_tone(inputs.get("desired_tone", "informative")),
        "blog_length": validate_blog_length(inputs.get("blog_length", "medium")),
        "seo_keywords": validate_keywords(inputs.get("seo_keywords")),
        "call_to_action": validate_non_empty(inputs.get("call_to_action"), "Call to action"),
        "industry": str(inputs.get("industry", "")).strip(),
        "avoid_claims": validate_optional_list(inputs.get("avoid_claims")),
        "brand_guidelines": str(inputs.get("brand_guidelines", "")).strip(),
    }
