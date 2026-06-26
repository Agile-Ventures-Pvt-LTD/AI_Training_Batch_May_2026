import requests
from typing import List, Dict, Optional
from datetime import date
import json

#=================TOOL 1=validate_city_input_tool===========================

def validate_city_input(
        city_name: str
):
    """Validates the city name entered by the user.
    This tool does not call the weather API.

    arguments:
        city_name: it take city name as argument"""

    if city_name != "":
        updated_city_name = city_name.strip()
        normalised_city_name = updated_city_name.replace(" ", "+")

        return {
            "success": True,
            "original_city_name": city_name,
            "normalized_city_name": normalised_city_name
        }

    if len(city_name.strip()) < 2 or city_name == "":
        return {
            "success": False,
            "message": "City name cannot be empty."
        }
    

    


#====================TOOL2 =fetching_weather_data========================

def get_weather_forecast(
        normalised_city_name: str
)->Dict[str, any]:
    """
    Calls the wttr.in JSON API and returns the raw weather response.
    This is the only tool that should call the external weather API.
    
    argument: 
        normalised_city_name: it is the normalised city name

    """

    url = f"https://wttr.in/{normalised_city_name}?format=j1"

    response = requests.get(url, timeout=10)
    
    data = response.json()

    if isinstance(data, dict) and "error" in data:
        return {

            "success": False,
            "city_name": "InvalidCity",
            "message": "Unable to fetch weather data."
        }


    
    return {
        "success": True,
        "city_name": normalised_city_name,
        "raw_weather_data": data}

# print(get_weather_forecast_tool('Delhi'))



#=======================TOOL3 normalize_weather_data_tool=========================

def norm_weather_data(
        raw_weather_data: Dict[str, any]
):
    """Converts raw wttr.in JSON into a clean internal weather schema.
        This tool must not call the external API.

        argument:
            raw_weather_data: it is the dictionary containing weather details

    """

    destination= raw_weather_data.nearest_area[0].areaName.value
    country= raw_weather_data.nearest_area[0].country[0].value
    current_condition=current_condition[0]

    return raw_weather_data
#  Convert numeric strings into int or float.
#  For each day, calculate max_wind_kmph from hourly[*].windspeedKmph.
#  For each day, calculate max_chance_of_rain from 


#=================TOOL 4 calculate_weather_risk_tool===================


def calculate_weather_risk(
        normalized_weather_data: Dict[str,any]
):
    """Calculates deterministic travel weather risk from normalized weather data.
    This tool must not call the API and must not use an LLM.

    argument: 
        normalised_weather_data: it is a normalised data in dictionary form 
        {
            "success": true,
            "destination": "Jaipur",
            "region": "Rajasthan",
            "country": "India",
            "forecast_days": 3,
            "current_weather": 
                    {
                    "temperature_c": 31.0,
                    "humidity": 48,
                    "precipitation_mm": 0.0,
                    "wind_speed_kmph": 12.0,
                    "weather_description": "Sunny"
                    },

            "daily_forecast": [
                    {
                    "date": "2026-06-26",
                    "max_temp_c": 37.0,
                    "min_temp_c": 27.0,
                    "avg_temp_c": 32.0,
                    "total_precipitation_mm": 1.2,
                    "max_wind_kmph": 28.0,
                    "max_chance_of_rain": 60,
                    "weather_description": "Partly cloudy"
                    }
                ]

        }

    """

    risk_factor=[]
    risks=[]
    recommended_actions=set()
    max_temp=normalized_weather_data.daily_forecast[0].max_temp_c
    total_precip=normalized_weather_data.daily_forecast[0].total_precipitation_mm
    max_chance_rain=normalized_weather_data.daily_forecast[0].total_precipitation_mm
    max_wind=normalized_weather_data.daily_forecast[0].max_wind_kmph

    if max_temp >= 40:
        risk_factor.append("High heat risk")
        risks.append('High')
        recommended_actions.add("Carry water and avoid long outdoor exposure during afternoon hours.")

    if 35 <= max_temp < 40:
        risk_factor.append("Moderate heat risk")
        risks.append('Moderate')
        recommended_actions.add("Carry water and avoid long outdoor exposure during afternoon hours.")

    if total_precip >= 20:
        risk_factor.append("High rain risk")
        risks.append('High')
        recommended_actions.add("Carry an umbrella or light rain protection.")

    if 5 <= total_precip< 20:
        risk_factor.append("Moderate rain risk")
        risks.append('Moderate')
        recommended_actions.add("Carry an umbrella or light rain protection.")

    if max_chance_rain >= 70:
        risk_factor.append("High rain probability")
        risks.append('Moderate')
        recommended_actions.add("Carry an umbrella or light rain protection.")

    if 40 <= max_chance_rain < 70:
        risk_factor.append("Moderate rain probability")
        risks.append('Moderate')
        recommended_actions.add("Carry an umbrella or light rain protection.")

    if max_wind >= 40:
        risk_factor.append("High wind risk")
        risks.append('High')
        recommended_actions.add("Avoid going outdoors.")
    
    if 25 <= max_wind < 40:
        risk_factor.append("Moderate wind risk")
        risks.append('Moderate')

    

    for risk in risks:
        if risk =='High':
            weather_risk='HIGH'
            break
        elif risk=='Moderate':
            weather_risk='MEDIUM'
        else:
            weather_risk='LOW'

    recommended_actions_required=list(recommended_actions)

    return {
        "weather_risk": weather_risk,
        "risk_factors": risk_factor,
        "recommended_actions": recommended_actions_required
        }


#===================TOOL 5 save_travel_advisory_tool==========================


def save_travel_advisory(
        report:Dict[str,any]
):
    """Saves the final advisory report as JSON.
        argument:
                report: it is the dictionary report input
    """
    with open(
        "outputs/travel_advisory_report.json", "w", encoding="utf-8"
    ) as f:

        json.dump(report, f, indent=2, ensure_ascii=False)
    
        






