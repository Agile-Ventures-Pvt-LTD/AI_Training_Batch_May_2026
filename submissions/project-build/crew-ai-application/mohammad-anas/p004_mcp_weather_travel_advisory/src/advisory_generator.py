try:
    from src.schemas import WeatherRisk
except ModuleNotFoundError:
    from schemas import WeatherRisk


def build_travel_readiness_advisory(weather_risk: str) -> str:
    if weather_risk == WeatherRisk.LOW:
        return "Travel appears comfortable based on the expected weather conditions."

    if weather_risk == WeatherRisk.MEDIUM:
        return (
            "Travel appears manageable with basic weather precautions."
        )

    return (
        "Travel is possible, but extra caution is recommended because "
        "of potentially severe weather conditions."
    )


def build_weather_risk_explanation(
    weather_risk: str,
    risk_factors: list[str],
) -> str:
    if not risk_factors:
        return "No significant weather risks were identified."

    reason = ", ".join(risk_factors)

    return (
        f"The overall weather risk is {weather_risk} because {reason.lower()}"
    )


def build_packing_suggestions(
    weather_risk: str,
    risk_factors: list[str],
) -> list[str]:
    suggestions = {
        "Water bottle",
        "Mobile phone charger",
    }

    text = " ".join(risk_factors).lower()

    if "temperature" in text or "heat" in text:
        suggestions.update(
            {
                "Cap or hat",
                "Sunscreen",
                "Light cotton clothing",
            }
        )

    if "rain" in text or "precipitation" in text:
        suggestions.update(
            {
                "Umbrella",
                "Raincoat",
                "Waterproof shoes",
            }
        )

    if "wind" in text:
        suggestions.add("Windproof jacket")

    if weather_risk == WeatherRisk.LOW:
        suggestions.add("Comfortable walking shoes")

    return sorted(suggestions)