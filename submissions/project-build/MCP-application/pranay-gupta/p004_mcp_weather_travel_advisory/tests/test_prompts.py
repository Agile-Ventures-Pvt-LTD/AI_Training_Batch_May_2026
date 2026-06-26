from prompts import (
    travel_readiness_prompt,
    weather_risk_summary_prompt,
    packing_recommendation_prompt,
    ALL_PROMPTS
)

def test_required_prompts_available():
    assert len(ALL_PROMPTS) == 3
    assert "travel_readiness_prompt" in ALL_PROMPTS
    assert "weather_risk_summary_prompt" in ALL_PROMPTS
    assert "packing_recommendation_prompt" in ALL_PROMPTS

def test_travel_readiness_prompt_content():
    result = travel_readiness_prompt(
        destination="Jaipur",
        weather_risk="MEDIUM",
        forecast_summary="Hot and partly cloudy",
        recommended_actions=["Carry water", "Use sunscreen"]
    )
    assert "Jaipur" in result
    assert "MEDIUM" in result
    assert "Hot and partly cloudy" in result
    assert "Carry water" in result
    assert "travel-readiness advisory" in result.lower()

def test_weather_risk_summary_prompt_content():
    result = weather_risk_summary_prompt(
        destination="Jaipur",
        weather_risk="MEDIUM",
        risk_factors=["High temperature expected"]
    )
    assert "Jaipur" in result
    assert "MEDIUM" in result
    assert "High temperature expected" in result
    assert "risk level" in result.lower()

def test_packing_recommendation_prompt_content():
    result = packing_recommendation_prompt(
        destination="Jaipur",
        weather_risk="MEDIUM",
        risk_factors=["High temperature expected"]
    )
    assert "Jaipur" in result
    assert "MEDIUM" in result
    assert "packing" in result.lower()
    assert "High temperature expected" in result