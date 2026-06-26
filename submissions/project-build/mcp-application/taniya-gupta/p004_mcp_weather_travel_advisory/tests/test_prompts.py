import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.prompts import (
    get_travel_readiness,
    get_weather_risk_summary,
    get_packing_recommendation
)

def test_get_travel_readiness():
    result = get_travel_readiness("Jaipur", "HIGH", "Hot", "Avoid noon")
    assert "Jaipur" in result
    assert "HIGH" in result
    assert "Hot" in result
    assert "Avoid noon" in result

def test_get_weather_risk_summary():
    result = get_weather_risk_summary("Pune", "MEDIUM", "Windy")
    assert "Pune" in result
    assert "MEDIUM" in result
    assert "Windy" in result

def test_get_packing_recommendation():
    result = get_packing_recommendation("Mumbai", "LOW", "No major risk")
    assert "Mumbai" in result
    assert "LOW" in result
    assert "No major risk" in result
