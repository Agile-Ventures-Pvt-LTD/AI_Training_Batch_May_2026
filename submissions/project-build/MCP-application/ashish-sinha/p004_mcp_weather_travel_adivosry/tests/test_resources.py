import json
import pytest
from src.resources import Checklist_Content,Advisory_Rule_Content,Forecast_Schema_Content

def test_static_checklist_resource():
    assert "Travel Readiness Checklist" in Checklist_Content
    assert "weather forecast" in Checklist_Content.lower()

def test_static_advisory_rules_resource():
    assert "LOW" in Advisory_Rule_Content
    assert "MEDIUM" in Advisory_Rule_Content
    assert "HIGH" in Advisory_Rule_Content

def test_static_schema_resource_is_valid_json():
    parsed_json = json.loads(Forecast_Schema_Content)
    assert "destination" in parsed_json
    assert "current_weather" in parsed_json
