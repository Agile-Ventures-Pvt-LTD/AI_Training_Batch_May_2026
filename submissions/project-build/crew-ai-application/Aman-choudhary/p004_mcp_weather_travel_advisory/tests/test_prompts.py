from prompts import (PROMPTS,travel_readiness_prompt,weather_risk_summary_prompt,packing_recommendation_prompt,)
def test_required_prompts_available():
    expected = {"travel_readiness_prompt","weather_risk_summary_prompt","packing_recommendation_prompt",}
    assert expected.issubset(set(PROMPTS.keys()))
def test_travel_readiness_prompt():
    prompt = travel_readiness_prompt(destination="Jaipur",weather_risk="MEDIUM",forecast_summary="Hot weather expected.",recommended_actions=["Carry water"],)
    assert "Jaipur" in prompt
    assert "MEDIUM" in prompt
def test_weather_risk_summary_prompt():
    prompt = weather_risk_summary_prompt(destination="Jaipur",weather_risk="HIGH",risk_factors=["Heavy rainfall"],)
    assert "HIGH" in prompt
    assert "Heavy rainfall" in prompt
def test_packing_recommendation_prompt():
    prompt = packing_recommendation_prompt(destination="Pune",weather_risk="LOW",risk_factors=[],)
    assert "Pune" in prompt