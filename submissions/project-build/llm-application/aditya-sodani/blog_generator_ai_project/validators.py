def validate_inputs(data: dict):

    errors = []

    if not data.get("blog_topic"):
        errors.append("Blog topic is required.")

    if not data.get("target_audience"):
        errors.append("Target audience is required.")

    if not data.get("product_or_service_context"):
        errors.append("Product or Service context is required.")

    key_points = data.get("key_points", [])

    if len(key_points) < 3:
        errors.append("Please provide at least 3 key points.")

    if not data.get("desired_tone"):
        errors.append("Desired tone is required.")

    if not data.get("blog_length"):
        errors.append("Blog length is required.")


    seo_keywords = data.get("seo_keywords",[])

    if len(seo_keywords) < 2:
        errors.append("At least 2 SEO keywords required.")

    if not data.get("call_to_action"):
        errors.append("Call to action is required.")

    if errors:
        raise ValueError("\n".join(errors))

    return True