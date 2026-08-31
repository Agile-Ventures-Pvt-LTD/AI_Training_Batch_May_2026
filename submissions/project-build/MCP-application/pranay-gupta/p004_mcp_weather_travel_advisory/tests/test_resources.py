from resources import (
    get_travel_checklist,
    get_advisory_rules,
    get_normalized_forecast_schema,
    CHECKLIST_URI,
    ADVISORY_RULES_URI,
    SCHEMA_URI,
    ALL_RESOURCES
)

def test_required_resources_available():
    assert len(ALL_RESOURCES) == 3
    assert CHECKLIST_URI in ALL_RESOURCES
    assert ADVISORY_RULES_URI in ALL_RESOURCES
    assert SCHEMA_URI in ALL_RESOURCES

def test_travel_checklist_content():
    content = get_travel_checklist()
    assert "Travel Readiness Checklist" in content
    assert "water" in content.lower()
    assert "umbrella" in content.lower()
    assert "phone charged" in content.lower()
    assert "essential documents" in content.lower()

def test_advisory_rules_content():
    content = get_advisory_rules()
    assert "LOW" in content
    assert "MEDIUM" in content
    assert "HIGH" in content
    assert "Normal travel precautions" in content
    assert "reconsider" in content.lower()

def test_normalized_forecast_schema_content():
    content = get_normalized_forecast_schema()
    assert "destination" in content
    assert "current_weather" in content
    assert "daily_forecast" in content
    assert "temperature_c" in content
    assert "max_chance_of_rain" in content