from src.prompts import get_realtime_weather

def test_tool():

    result = get_realtime_weather("Mumbai")

    required_keys = [
        "city",
        "country",
        "temperature",
        "condition",
        "humidity"
    ]

    for key in required_keys:
        assert key in result

    print("✅ Prompts Validation Passed")

if __name__ == "__main__":
    test_tool()