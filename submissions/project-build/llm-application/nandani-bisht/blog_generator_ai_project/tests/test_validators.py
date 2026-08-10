from validators import validate_inputs


def test_validate_inputs_success():
    data = {
        "blog_topic": "Why ACME matters",
        "target_audience": "SaaS marketers",
        "seo_keywords": ["acme", "marketing"],
        "key_points": ["point1", "point2", "point3"],
        "call_to_action": "Contact sales"
    }
    errors = validate_inputs(data)
    assert errors == []


def test_validate_inputs_errors():
    data = {
        "blog_topic": "",
        "target_audience": "",
        "seo_keywords": ["onlyone"],
        "key_points": ["one"],
        "call_to_action": ""
    }
    errors = validate_inputs(data)
    assert "Blog Topic is required" in errors
    assert "Target Audience is required" in errors
    assert "Minimum 2 SEO keywords required" in errors
    assert "Minimum 3 key points required" in errors
    assert "Call To Action is required" in errors
