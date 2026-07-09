from resources import (RESOURCES,get_resource,)
def test_required_resources_available():
    expected = {
        "resource://travel/checklist",
        "resource://travel/advisory-rules",
        "resource://weather/normalized-forecast-schema",
    }
    assert expected.issubset(set(RESOURCES.keys()))
def test_get_travel_checklist():
    data = get_resource("resource://travel/checklist")
    assert "Travel Readiness Checklist" in data
def test_get_advisory_rules():
    data = get_resource("resource://travel/advisory-rules")
    assert "LOW" in data
    assert "MEDIUM" in data
    assert "HIGH" in data