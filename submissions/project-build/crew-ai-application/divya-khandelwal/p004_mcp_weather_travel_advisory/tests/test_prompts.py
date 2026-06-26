import src.prompts as p

def test_required_prompts_available():
    p1 = p.travel_readiness_prompt("Jaipur", "MEDIUM", "Warm", ["Carry water"])
    p2 = p.weather_risk_summary_prompt("Jaipur", "MEDIUM", ["High heat"])
    p3 = p.packing_recommendation_prompt("Jaipur", "MEDIUM", ["High heat"])
    
    assert "Destination: Jaipur" in p1
    assert "Risk Level: MEDIUM" in p2
    assert "packing suggestions" in p3.lower()
