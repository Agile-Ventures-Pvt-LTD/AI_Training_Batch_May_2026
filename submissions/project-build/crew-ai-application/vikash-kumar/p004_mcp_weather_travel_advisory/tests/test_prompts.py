from src.prompts import travel_readiness_prompt

def test_required_prompts_available():
    prompt_test = travel_readiness_prompt("Jaipur", "MEDIUM", "Partly cloudy", ["Carry umbrella"])
    assert "Jaipur" in prompt_test
    assert "MEDIUM" in prompt_test
