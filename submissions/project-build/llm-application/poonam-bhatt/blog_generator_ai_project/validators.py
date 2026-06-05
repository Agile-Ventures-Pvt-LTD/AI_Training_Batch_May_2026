# 


def validate_blog_input(data):

    errors = []

    if not data["blog_topic"].strip():
        errors.append("Blog topic cannot be empty.")

    if not data["target_audience"].strip():
        errors.append("Target audience cannot be empty.")

    if len(data["key_points"]) < 3:
        errors.append(
            "Please provide at least 3 key points before generating the blog."
        )

    valid_lengths = [
        "short",
        "medium",
        "long"
    ]

    if data["blog_length"].lower() not in valid_lengths:
        errors.append(
            "Blog length must be short, medium, or long."
        )

    if len(data["seo_keywords"]) < 2:
        errors.append(
            "Please provide at least 2 SEO keywords."
        )

    if not data["call_to_action"].strip():
        errors.append(
            "Call to action cannot be empty."
        )

    return errors