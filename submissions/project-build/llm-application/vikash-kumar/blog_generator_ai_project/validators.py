from typing import Dict, List


def validate_blog_input(
    payload: Dict
) -> List[str]:

    errors = []

    if not payload.get("blog_topic"):
        errors.append(
            "Blog topic cannot be empty."
        )

    if not payload.get("target_audience"):
        errors.append(
            "Target audience cannot be empty."
        )

    if not payload.get(
        "product_or_service_context"
    ):
        errors.append(
            "Product/service context cannot be empty."
        )

    key_points = payload.get(
        "key_points",
        []
    )

    if len(key_points) < 3:
        errors.append(
            "Please provide at least 3 key points before generating the blog."
        )

    blog_length = (
        payload.get(
            "blog_length",
            ""
        )
        .lower()
        .strip()
    )

    valid_lengths = [
        "short",
        "medium",
        "long"
    ]

    if blog_length not in valid_lengths:
        errors.append(
            f"Blog length must be one of: {valid_lengths}"
        )

    seo_keywords = payload.get(
        "seo_keywords",
        []
    )

    if len(seo_keywords) < 2:
        errors.append(
            "Provide at least 2 SEO keywords."
        )

    if not payload.get(
        "call_to_action"
    ):
        errors.append(
            "Call to action cannot be empty."
        )

    return errors