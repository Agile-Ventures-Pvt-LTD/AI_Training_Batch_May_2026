import json
from schemas import NormalizedWeatherData, CurrentWeather, DailyForecast

def validate_city_input_tool(city_name: str) -> dict:
    short = city_name.strip()
    if not short:
        return {"success": False, "message": "City name can not be empty."}
    if len(short) < 2:
        return {"success": False, "message": "City name can not be shorter than 2 characters"}
    normalized = short.replace(" ", "+")
    return {"success": True,"original_city_name": short,"normalized_city_name": normalized}

def get_weather_forecast_tool(normalized_city_name: str) -> dict:
    from api_client import get_weather_from_wttr
    weather_forecast = get_weather_from_wttr(normalized_city_name)
    if not weather_forecast.get("success"):
        return {"success": False, "city_name": normalized_city_name, "message": "Unable to fetch weather data."}
    return {"success": True,"city_name": normalized_city_name,"raw_weather_data": weather_forecast["raw_weather_data"]}

def normalize_weather_data_tool(raw_weather_data: dict) -> dict:
    try:
        nearest = raw_weather_data["nearest_area"][0]
        current = raw_weather_data["current_condition"][0]
        weather_list = raw_weather_data["weather"][:3]
        dest = nearest["areaName"][0]["value"]
        region = nearest["region"][0]["value"]
        country = nearest["country"][0]["value"]
        current_weather = {"temperature_c": float(current["temp_C"]),"humidity": int(current["humidity"]),"precipitation_mm": float(current["precipMM"]),"wind_speed_kmph": float(current["windspeedKmph"]),"weather_description": current["weatherDesc"][0]["value"]}
        daily_forecast = []
        for day in weather_list:
            hours = day["hourly"]
            max_wind = max(float(h["windspeedKmph"]) for h in hours)
            max_rain_chance = max(int(h["chanceofrain"]) for h in hours)
            total_precip = sum(float(h["precipMM"]) for h in hours)
            daily_forecast.append({"date": day["date"],"max_temp_c": float(day["maxtempC"]),"min_temp_c": float(day["mintempC"]),"avg_temp_c": float(day["avgtempC"]),
                "total_precipitation_mm": round(total_precip, 2),"max_wind_kmph": max_wind,"max_chance_of_rain": max_rain_chance,"weather_description": hours[0]["weatherDesc"][0]["value"]})
            
        report = {"success": True,"destination": dest,
            "region": region,"country": country,"forecast_days": len(daily_forecast),"current_weather": current_weather,"daily_forecast": daily_forecast}
        return report
    except Exception:
        return {"success": False, "message": "Unable to normalize weather data because required fields are missing"}

def calculate_weather_risk_tool(normalized_weather_data: dict) -> dict:
    risk_factors = []
    recommended_actions = []
    max_temp = max(day["max_temp_c"] for day in normalized_weather_data["daily_forecast"])
    max_precip = max(day["total_precipitation_mm"] for day in normalized_weather_data["daily_forecast"])
    max_chance = max(day["max_chance_of_rain"] for day in normalized_weather_data["daily_forecast"])
    max_wind = max(day["max_wind_kmph"] for day in normalized_weather_data["daily_forecast"])
    high_risk = False
    med_risk = False

    if max_temp >= 40:
        high_risk = True
        risk_factors.append("Maximum temperature is expected to be critically high")
        recommended_actions.append("Don't go outside and drink water. Go in emergency")
    elif 35 <= max_temp < 40:
        med_risk = True
        risk_factors.append("Maximum temperature is expected to be above 35°C.")
        recommended_actions.append("Try not go out in afternoon")

    if max_precip >= 20:
        high_risk = True
        risk_factors.append("Heavy rain precipitation is expected ")
        recommended_actions.append("Don't go outside, it's raining a lot")
    elif 5 <= max_precip < 20:
        med_risk = True
        risk_factors.append("Moderate rain precipitation is expected.")
        recommended_actions.append("Carry an umbrella")

    if max_chance >= 70:
        high_risk = True
        risk_factors.append("Very high probability of rain during your travel dates.")
    elif 40 <= max_chance < 70:
        med_risk = True
        risk_factors.append("Chance of rain may increase , so try to be indoor")

    if max_wind >= 40:
        high_risk = True
        risk_factors.append("High wind hazards are expected")
        recommended_actions.append("Avoid open,roof or outside the house")
    elif 25 <= max_wind < 40:
        med_risk = True
        risk_factors.append("Wind speed is moderate")
        recommended_actions.append("Try to go for the emergency work outside")

    overall_risk = "LOW"
    if high_risk:
        overall_risk = "HIGH"
    elif med_risk:
        overall_risk = "MEDIUM"
        
    return {"weather_risk": overall_risk,"risk_factors": risk_factors if risk_factors else ["No major weather hazards detected."],"recommended_actions": recommended_actions if recommended_actions else ["It is good but be cautious"]}

import os

def save_travel_advisory_tool(report: dict):
    # import os
    os.makedirs("outputs", exist_ok=True)
    path = "outputs/travel_advisory_report.json"
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    return {"success": True, "saved_path": path}


def save_travel_advisory_tool(report: dict, filename: str = "travel_advisory_report.json") -> dict:
    """It will save the travel advisory in json format"""
    output_dir = "outputs"
    if "sample_" in filename:
        output_dir = "sample_outputs"
        
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    return {"success": True,"saved_path": file_path}
