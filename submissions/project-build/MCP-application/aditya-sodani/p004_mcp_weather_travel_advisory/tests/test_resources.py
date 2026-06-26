from src.resources import get_checklist, get_advisory_rules, get_schema


def test_required_resources_available():
    checklist = get_checklist()
    rules = get_advisory_rules()
    schema = get_schema()

    assert "Travel" in checklist
    assert "LOW" in rules
    assert "destination" in schema