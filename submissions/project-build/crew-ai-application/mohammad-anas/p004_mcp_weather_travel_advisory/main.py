import sys

from src.advisory_generator import (
    build_packing_suggestions,
    build_travel_readiness_advisory,
    build_weather_risk_explanation,
)
from src.tools import get_registered_tools

TOOLS_USED = [
    "validate_city_input_tool",
    "get_weather_forecast_tool",
    "normalize_weather_data_tool",
    "calculate_weather_risk_tool",
    "save_travel_advisory_tool",
]

RESOURCES_USED = [
    "resource://travel/checklist",
    "resource://travel/advisory-rules",
    "resource://weather/normalized-forecast-schema",
]

PROMPTS_USED = [
    "travel_readiness_prompt",
    "weather_risk_summary_prompt",
    "packing_recommendation_prompt",
]


def fail(step: str, response: dict) -> None:
    print(f"{step} failed")
    print(response)
    raise SystemExit(1)


def main() -> None:
    city = (
        sys.argv[1]
        if len(sys.argv) > 1
        else input("Destination city: ").strip()
    )

    tools = get_registered_tools()

    validate = tools["validate_city_input_tool"]
    weather = tools["get_weather_forecast_tool"]
    normalize = tools["normalize_weather_data_tool"]
    calculate = tools["calculate_weather_risk_tool"]
    save = tools["save_travel_advisory_tool"]

    print(f"\nGenerating travel advisory for {city}\n")

    validation = validate(city)
    if not validation["success"]:
        fail("Validation", validation)

    weather_response = weather(validation["normalized_city_name"])
    if not weather_response["success"]:
        fail("Weather API", weather_response)

    normalized = normalize(weather_response["raw_weather_data"])
    normalized.pop("success", None)
    if not normalized.get("success", True):
        fail("Normalization", normalized)

    risk = calculate(normalized)

    report = {
        **normalized,
        **risk,
        "packing_suggestions": build_packing_suggestions(
            risk["weather_risk"],
            risk["risk_factors"],
        ),
        "travel_readiness_advisory": build_travel_readiness_advisory(
            risk["weather_risk"],
        ),
        "weather_risk_explanation": build_weather_risk_explanation(
            risk["weather_risk"],
            risk["risk_factors"],
        ),
        "resources_used": RESOURCES_USED,
        "tools_used": TOOLS_USED,
        "prompts_used": PROMPTS_USED,
    }

    result = save(report)

    if not result["success"]:
        fail("Saving report", result)

    print("\nTravel advisory generated successfully.")
    print(result["saved_path"])


if __name__ == "__main__":
    main()