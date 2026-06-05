from validators import (
    validate_blog_input
)


def test_validation_success():

    payload = {
        "blog_topic": "AI",
        "target_audience": "Managers",
        "product_or_service_context":
        "AI Tool",

        "key_points": [
            "Point 1",
            "Point 2",
            "Point 3"
        ],

        "blog_length":
        "medium",

        "seo_keywords": [
            "AI",
            "Automation"
        ],

        "call_to_action":
        "Book Demo"
    }

    errors = validate_blog_input(
        payload
    )

    assert len(errors) == 0


def test_validation_failure():

    payload = {}

    errors = validate_blog_input(
        payload
    )

    assert len(errors) > 0