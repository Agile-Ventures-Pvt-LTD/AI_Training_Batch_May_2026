

def validate_inputs(prompt_details: dict):

    blog_topic = prompt_details.get("blog_topic")
    target_audience = prompt_details.get("target_audience")
    product_or_service_context = prompt_details.get("product_or_service_context")
    key_points = prompt_details.get("key_points")
    desired_tone = prompt_details.get("desired_tone")
    blog_length = prompt_details.get("blog_length")
    seo_keywords = prompt_details.get("seo_keywords")
    call_to_action = prompt_details.get("call_to_action")

    # Required field validation

    if not blog_topic:
        raise ValueError("Blog topic is required.")

    if not target_audience:
        raise ValueError("Target audience is required.")

    if not product_or_service_context:
        raise ValueError("Product or service context is required.")

    if not key_points:
        raise ValueError("At least 3 key points are required.")

    if len(key_points) < 3:
        raise ValueError(
            "Please provide at least 3 key points before generating the blog."
        )

    if not desired_tone:
        raise ValueError("Desired tone is required.")

    if not blog_length:
        raise ValueError("Blog length is required.")

    if not seo_keywords:
        raise ValueError("At least 2 SEO keywords are required.")

    if len(seo_keywords) < 2:
        raise ValueError(
            "Please provide at least 2 SEO keywords."
        )

    if not call_to_action:
        raise ValueError("Call to action is required.")

    return True