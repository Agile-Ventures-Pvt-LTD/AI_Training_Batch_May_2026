def validate_inputs(data):
    errors = []

    if not data.get("blog_topic"):
        errors.append("Blog Topic is required")

    if not data.get("target_audience"):
        errors.append("Target Audience is required")

    if not isinstance(data.get("seo_keywords", []), list) or len(data.get("seo_keywords", [])) < 2:
        errors.append("Minimum 2 SEO keywords required")

    if not isinstance(data.get("key_points", []), list) or len(data.get("key_points", [])) < 3:
        errors.append("Minimum 3 key points required")

    if not data.get("call_to_action"):
        errors.append("Call To Action is required")

    return errors
