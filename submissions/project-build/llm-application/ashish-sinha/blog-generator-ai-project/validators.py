def validate_inputs(data):

    if not data["blog_topic"]:
        raise ValueError(
            "Blog topic cannot be empty"
        )

    if not data["target_audience"]:
        raise ValueError(
            "Target audience required"
        )

    if len(data["key_points"]) < 3:
        raise ValueError(
            "Provide at least 3 key points"
        )

    if len(data["seo_keywords"]) < 2:
        raise ValueError(
            "Provide at least 2 SEO keywords"
        )

    if not data["call_to_action"]:
        raise ValueError(
            "Call To Action required"
        )

    return True