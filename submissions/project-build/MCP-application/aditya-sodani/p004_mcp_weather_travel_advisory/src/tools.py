from src.api_client import get_weather_from_wttr


def validate_city_input_tool(input_data):
    city = input_data.get("city_name", "").strip()

    if not city:
        return {"success": False, "message": "City empty"}

    return {
        "success": True,
        "original_city_name": city,
        "normalized_city_name": city.replace(" ", "+")
    }


def get_weather_forecast_tool(input_data):
    return get_weather_from_wttr(input_data["normalized_city_name"])


def normalize_weather_data_tool(input_data):
    try:
        raw = input_data["raw_weather_data"]

        area = raw["nearest_area"][0]
        current = raw["current_condition"][0]

        days = []
        for d in raw["weather"][:3]:
            winds = [float(h["windspeedKmph"]) for h in d["hourly"]]
            rains = [float(h["precipMM"]) for h in d["hourly"]]
            chances = [int(h["chanceofrain"]) for h in d["hourly"]]

            days.append({
                "date": d["date"],
                "max_temp_c": float(d["maxtempC"]),
                "min_temp_c": float(d["mintempC"]),
                "avg_temp_c": float(d["avgtempC"]),
                "total_precipitation_mm": sum(rains),
                "max_wind_kmph": max(winds),
                "max_chance_of_rain": max(chances),
                "weather_description": d["hourly"][0]["weatherDesc"][0]["value"]
            })

        return {
            "success": True,
            "destination": area["areaName"][0]["value"],
            "region": area["region"][0]["value"],
            "country": area["country"][0]["value"],
            "forecast_days": len(days),
            "current_weather": {
                "temperature_c": float(current["temp_C"]),
                "humidity": int(current["humidity"]),
                "precipitation_mm": float(current["precipMM"]),
                "wind_speed_kmph": float(current["windspeedKmph"]),
                "weather_description": current["weatherDesc"][0]["value"]
            },
            "daily_forecast": days
        }
    except:
        return {"success": False}


def calculate_weather_risk_tool(input_data):
    data = input_data["normalized_weather_data"]

    risk = "LOW"
    factors = []
    actions = []

    for d in data["daily_forecast"]:
        if d["max_temp_c"] >= 40:
            risk = "HIGH"
            factors.append("Extreme heat")
        elif d["max_temp_c"] >= 35:
            risk = "MEDIUM"
            factors.append("High heat")

    if risk == "MEDIUM":
        actions.append("Carry water")
    if risk == "HIGH":
        actions.append("Avoid outdoor travel")

    return {
        "weather_risk": risk,
        "risk_factors": factors,
        "recommended_actions": actions
    }


def save_travel_advisory_tool(input_data):
    import os, json

    os.makedirs("outputs", exist_ok=True)
    path = "outputs/travel_advisory_report.json"

    with open(path, "w") as f:
        json.dump(input_data["report"], f, indent=2)

    return {"success": True, "saved_path": path}