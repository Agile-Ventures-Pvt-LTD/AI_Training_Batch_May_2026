def validate_inputs(data: dict) -> list:
    """Simple validator for blog generator inputs.

    Returns a list of error messages (empty list = valid).
    """
    errors = []
    topic = str(data.get("blog_topic", "")).strip()
    audience = str(data.get("target_audience", "")).strip()
    product = str(data.get("product_or_service_context", "")).strip()
    tone = str(data.get("desired_tone", "")).strip()
    key_points = data.get("key_points") or []
    blog_length = str(data.get("blog_length", "")).strip()
    seo_keywords = data.get("seo_keywords") or []
    cta = str(data.get("call_to_action", "")).strip()

    if not topic:
        errors.append("blog_topic is required.")
    if not audience:
        errors.append("target_audience is required.")
    if not product:
        errors.append("product_or_service_context is required.")
    if not tone:
        errors.append("desired_tone is required.")
    if not isinstance(key_points, list) or len([k for k in key_points if str(k).strip()]) < 3:
        errors.append("At least 3 key_points are required.")
    if not blog_length:
        errors.append("blog_length is required.")
    if not isinstance(seo_keywords, list) or len([k for k in seo_keywords if str(k).strip()]) < 2:
        errors.append("At least 2 seo_keywords are required.")
    if not cta:
        errors.append("call_to_action is required.")

    return errors


