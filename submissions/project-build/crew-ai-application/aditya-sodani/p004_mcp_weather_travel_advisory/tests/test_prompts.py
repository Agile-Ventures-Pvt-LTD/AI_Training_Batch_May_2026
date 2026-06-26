from src.prompts import (
    travel_readiness_prompt,
    weather_risk_summary_prompt,
    packing_recommendation_prompt
)


def test_travel_readiness_prompt():
    res = travel_readiness_prompt({
        "destination": "Jaipur",
        "weather_risk": "LOW",
        "forecast_summary": "",
        "recommended_actions": []
    })

    assert "Jaipur" in res


def test_weather_risk_summary_prompt():
    res = weather_risk_summary_prompt({
        "destination": "Jaipur",
        "weather_risk": "MEDIUM",
        "risk_factors": ["Heat"]
    })

    assert "MEDIUM" in res


def test_packing_recommendation_prompt():
    res = packing_recommendation_prompt({
        "destination": "Jaipur",
        "weather_risk": "HIGH",
        "risk_factors": []
    })

    assert isinstance(res, list)
    assert len(res) > 0