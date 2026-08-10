from validators import validate_inputs


def test_valid_input():

    data = {
        "blog_topic": "AI in Customer Support",
        "target_audience": "Support Managers",
        "product_or_service_context": "AI Assistant",
        "key_points": [
            "Point 1",
            "Point 2",
            "Point 3"
        ],
        "desired_tone": "Professional",
        "blog_length": "900 words",
        "seo_keywords": [
            "AI support",
            "support automation"
        ],
        "call_to_action": "Book a Demo"
    }

    assert validate_inputs(data) == True


def test_missing_blog_topic():

    data = {
        "blog_topic": "",
        "target_audience": "Support Managers",
        "product_or_service_context": "AI Assistant",
        "key_points": [
            "Point 1",
            "Point 2",
            "Point 3"
        ],
        "desired_tone": "Professional",
        "blog_length": "900 words",
        "seo_keywords": [
            "AI support",
            "support automation"
        ],
        "call_to_action": "Book a Demo"
    }

    try:
        validate_inputs(data)
        assert False

    except ValueError:
        assert True