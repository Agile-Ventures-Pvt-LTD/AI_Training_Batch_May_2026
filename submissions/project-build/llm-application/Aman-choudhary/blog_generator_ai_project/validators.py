def validate_input(data):
    if not data.get("blog_topic"):
        raise ValueError(
            "Blog topic cannot be empty."
        )
    if not data.get("target_audience"):
        raise ValueError(
            "Target audience cannot be empty."
        )
    if len(data.get("key_points", [])) < 3:
        raise ValueError(
            "Provide at least 3 key points"
        ) 
    if len(data.get("seo_keywords", [])) < 2:
        raise ValueError(
            "Provide at least 2 SEO keywords"
        )
    if not data.get("call_to_action"):
        raise ValueError(
            "Call to Action cannot be empty"
        )
    return True