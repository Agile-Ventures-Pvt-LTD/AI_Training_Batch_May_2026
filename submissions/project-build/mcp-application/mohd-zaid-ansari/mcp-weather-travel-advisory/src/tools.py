import json 
import requests
from typing import Any, List, Dict, Optional 
from fastmcp import FastMCP
from pathlib import Path
import os
from dotenv import load_dotenv
from src.server import mcp

@mcp.tool()
async def validate_city_input_tool(city_name: str) -> Dict[str, Any]:
    """
    Validate the name of the city and normalize it. 
    Replaces spaces with '+' for safe API URL construction.
    """
    if not city_name:
        return {
            "success": False,
            "message": "City name cannot be empty."
        }
    original = city_name.strip()
    if not original:
        return {
            "success": False,
            "message": "City cannot be empty."
        }
    if len(original) < 3:
        return {
            "success": False,
            "message": "City name must be of atleast 3 characters."
        }
    normalized = "+".join([word for word in original.split(" ") if word])
    
    return {
        "success": True,
        "original_city_name": original,
        "normalized_city_name": normalized
    }


#=================================================================================================================================

@mcp.tool()
async def get_weather_forecast_tool(normalized_city_name: str) -> Dict[str, Any]:
    """
    You have to call the wttr.in JSON API and return the raw response weather.
    please implement domain fallbacks and handle excption.
    """
    primary_url = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
    fallback_url = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")

    urls = [
        f"{primary_url}/{normalized_city_name}?format=j1",
        f"{fallback_url}/{normalized_city_name}?format=j1"
    ]
    error_message = "No endpoints attempted."
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                raw_json = response.json()
                return {
                    "success": True,
                    "city_name": normalized_city_name,
                    "raw_weather_data": raw_json
                }
            else:
                error_message = f"HTTP Error Status Code: {response.status_code}"
        except requests.Timeout:
            error_message = "Connection attempt timed out after 10 seconds."
        except requests.RequestException as error:
            error_message = f"Network layer exception: {str(error)}"
        except ValueError:
            error_message = "Remote endpoint returned non-parseable JSON payload strings."
    return {
        "success": False,
        "city_name": normalized_city_name,
        "message": f"Unable to fetch weather data. Details: {error_message}"
    }

#=================================================================================================================================
@mcp.tool()
async def normalize_weather_data_tool(raw_weather_data: Dict[str,Any]) -> Dict[str,Any]:
    """
    Your task is to convert the wttr.in JSON in a clean internal weather schema.
    Do it effeciently and give a structured and clean weather schema.
    """
    try:
        area=raw_weather_data["nearest_area"][0]
        destination=area["areaName"][0]["value"]
        region=area["region"][0]["value"]
        country=area["country"][0]["value"]

        current_scenerio = raw_weather_data["current_condition"][0]
        current_weather = {
            "temperature_c": float(current_scenerio["temp_C"]),
            "humidity": int(current_scenerio["humidity"]),
            "precipitation_mm": float(current_scenerio["precipMM"]),
            "wind_speed_kmph": float(current_scenerio["windspeedKmph"]),
            "weather_description": current_scenerio["weatherDesc"][0]["value"]
        }

        daily_forecast = []
        weather_days = raw_weather_data.get("weather", [])
        
        for day in weather_days[:3]:
            hourly_list = day.get("hourly", [])
            winds = [float(h["windspeedKmph"]) for h in hourly_list if "windspeedKmph" in h]
            chances = [int(h["chanceofrain"]) for h in hourly_list if "chanceofrain" in h]
            precips = [float(h["precipMM"]) for h in hourly_list if "precipMM" in h]
            max_wind = max(winds) if winds else 0.0
            max_chance = max(chances) if chances else 0
            total_precip = sum(precips) if precips else 0.0
            desc = "Variable"
            if hourly_list and "weatherDesc" in hourly_list[0] and hourly_list[0]["weatherDesc"]:
                desc = hourly_list[0]["weatherDesc"][0]["value"]

            day_data = {
                "date": day["date"],
                "max_temp_c": float(day["maxtempC"]),
                "min_temp_c": float(day["mintempC"]),
                "avg_temp_c": float(day["avgtempC"]),
                "total_precipitation_mm": round(total_precip, 2),
                "max_wind_kmph": max_wind,
                "max_chance_of_rain": max_chance,
                "weather_description": desc
            }
            daily_forecast.append(day_data)
            
        return {
            "success": True,
            "destination": destination,
            "region": region,
            "country": country,
            "forecast_days": len(daily_forecast),
            "current_weather": current_weather,
            "daily_forecast": daily_forecast
        }
        
    except (KeyError, IndexError, ValueError, TypeError) as error:
        return {
            "success": False,
            "message": f"Unable to normalize weather data because required fields are missing. Error details: {str(error)}"
        }

                

#=================================================================================================================================
@mcp.tool()
async def calculate_weather_risk_tool(normalize_weather_data: Dict[str,Any]) -> Dict[str,Any]:
    """
    Calcutate deterministic travel weather risk from mormalized weather data.
    Categories the risk level of the different weather in HIGH, MEDIUM, LOW.
    You must not implements and API tool call.
    """
    forecasts=normalize_weather_data.get("daily_forecast", [])
    max_temp=max([d["max_temp_c"] for d in forecasts]) if forecasts else 0.0
    max_precipitation=max([d["total_precipitation_mm"] for d in forecasts]) if forecasts else 0.0
    max_chance_rain=max([d["max_chance_of_rain"] for d in forecasts]) if forecasts else 0.0
    max_wind=max([d["max_wind_kmph"] for d in forecasts]) if forecasts else 0.0

    risk=[]
    recommended_action=[]
    overall_risk="LOW"

    if max_temp>=40.0 or max_precipitation>=20.0 or max_chance_rain>=70.0 or max_wind>=40:
        overall_risk="HIGH"
    elif 35.0<=max_temp< 40.0 or 5<=max_precipitation<20 or 40<=max_chance_rain<70 or 25<=max_wind<40:
        overall_risk="MEDIUM"
    else:
        overall_risk="LOW"
    
    return{
        "weather_risk":overall_risk
    }

#================================================================================================================================

@mcp.tool()
async def save_travel_advisory_tool(report:Dict[str,Any]) -> Dict[str,Any]:
    """
    Save the final report of the travel as a Structured JSON file.
    """
    try:
        output_dir=os.getenv("OUTPUT_PATH","outputs")
        os.makedirs(output_dir, exist_ok=True)
        saved_path=os.path.join(output_dir, "travel_advisory_report.json")
        with open(saved_path, "w", encoding="utf-8") as file_out:
            json.dump(report, file_out, indent=2, ensure_ascii=False)
        return{
            "success":True,
            "saved_path":saved_path
        }
    except Exception as e:
        return{
            "success":True,
            "message":"Failed to save the report."
        }


#=================================================================================================================================
# # Temporary manual test execution harness
# if __name__ == "__main__":
#     import asyncio
    
#     async def run_test():
#         print("[*] Testing Tool 1 with a valid multi-word city...")
#         res1 = await validate_city_input_tool("  New Delhi  ")
#         print("Result 1:", res1)
        
#         print("\n[*] Testing Tool 1 with an invalid empty string...")
#         res2 = await validate_city_input_tool("   ")
#         print("Result 2:", res2)
        
#         print("\n[*] Testing Tool 1 with a short name...")
#         res3 = await validate_city_input_tool("X")
#         print("Result 3:", res3)

#     asyncio.run(run_test())

# Temporary manual validation engine for Tool 2
# if __name__ == "__main__":
#     import asyncio
#     from dotenv import load_dotenv
#     from pathlib import Path
    
#     # Force load environment context explicitly for standalone runner tests
#     ROOT_DIR = Path(__file__).parent.resolve().parent
#     load_dotenv(dotenv_path=ROOT_DIR / ".env")

#     async def test_network_tool():
#         print("[*] Dispatching real-time network request for 'Jaipur'...")
#         response = await get_weather_forecast_tool("Jaipur")
        
#         print(f"\n[+] Request Success Status: {response['success']}")
#         print(f"[+] City Query Tracked: {response['city_name']}")
        
#         if response["success"]:
#             # Isolate and inspect top-level payload keys specified by the PRD
#             raw_data = response["raw_weather_data"]
#             sections = list(raw_data.keys())
#             print(f"[+] Extracted JSON Data Sections: {sections}")
            
#             # Print localized current temperatures to verify data accuracy
#             current_temp = raw_data["current_condition"][0]["temp_C"]
#             print(f"[+] Real-Time Temperature in Jaipur: {current_temp}°C")
#         else:
#             print(f"[!] Network Pipeline Failure Message: {response['message']}")

#     asyncio.run(test_network_tool())


# from typing import Any, Dict
# from src.server import mcp

# @mcp.tool()
# async def normalize_weather_data_tool(raw_weather_data: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Converts nested raw wttr.in JSON data into a clean internal weather schema.
#     Enforces numeric casting and hourly sequence calculations.
#     """
#     try:
#         # 1. Safely pull location details from the arrays
#         area_node = raw_weather_data["nearest_area"][0]
#         destination = area_node["areaName"][0]["value"]
#         region = area_node["region"][0]["value"]
#         country = area_node["country"][0]["value"]
        
#         # 2. Extract and cast current weather conditions
#         current_node = raw_weather_data["current_condition"][0]
#         current_weather = {
#             "temperature_c": float(current_node["temp_C"]),
#             "humidity": int(current_node["humidity"]),
#             "precipitation_mm": float(current_node["precipMM"]),
#             "wind_speed_kmph": float(current_node["windspeedKmph"]),
#             "weather_description": current_node["weatherDesc"][0]["value"]
#         }
        
#         # 3. Process up to 3 days of forecast arrays
#         daily_forecast = []
#         weather_days = raw_weather_data.get("weather", [])
        
#         for day in weather_days[:3]:
#             hourly_list = day.get("hourly", [])
            
#             # Aggregate and compute hourly performance thresholds
#             winds = [float(h["windspeedKmph"]) for h in hourly_list if "windspeedKmph" in h]
#             chances = [int(h["chanceofrain"]) for h in hourly_list if "chanceofrain" in h]
#             precips = [float(h["precipMM"]) for h in hourly_list if "precipMM" in h]
            
#             max_wind = max(winds) if winds else 0.0
#             max_chance = max(chances) if chances else 0
#             total_precip = sum(precips) if precips else 0.0
            
#             # Safely grab a fallback description text string
#             desc = "Variable"
#             if hourly_list and "weatherDesc" in hourly_list[0] and hourly_list[0]["weatherDesc"]:
#                 desc = hourly_list[0]["weatherDesc"][0]["value"]
                
#             day_data = {
#                 "date": day["date"],
#                 "max_temp_c": float(day["maxtempC"]),
#                 "min_temp_c": float(day["mintempC"]),
#                 "avg_temp_c": float(day["avgtempC"]),
#                 "total_precipitation_mm": round(total_precip, 2),
#                 "max_wind_kmph": max_wind,
#                 "max_chance_of_rain": max_chance,
#                 "weather_description": desc
#             }
#             daily_forecast.append(day_data)
            
#         return {
#             "success": True,
#             "destination": destination,
#             "region": region,
#             "country": country,
#             "forecast_days": len(daily_forecast),
#             "current_weather": current_weather,
#             "daily_forecast": daily_forecast
#         }
        
#     except (KeyError, IndexError, ValueError, TypeError) as error:
#         return {
#             "success": False,
#             "message": f"Unable to normalize weather data because required fields are missing. Error details: {str(error)}"
#         }


# Temporary manual test execution harness for Tool 3
# if __name__ == "__main__":
#     import asyncio
    
#     # 1. Create a minimal mock response mimicking raw wttr.in payload strings
#     mock_raw_api_data = {
#         "current_condition": [{
#             "temp_C": "31",
#             "humidity": "48",
#             "precipMM": "0.0",
#             "windspeedKmph": "12",
#             "weatherDesc": [{"value": "Sunny"}]
#         }],
#         "nearest_area": [{
#             "areaName": [{"value": "Jaipur"}],
#             "region": [{"value": "Rajasthan"}],
#             "country": [{"value": "India"}]
#         }],
#         "weather": [{
#             "date": "2026-06-26",
#             "maxtempC": "37",
#             "mintempC": "27",
#             "avgtempC": "32",
#             "totalSnow_cm": "0.0",
#             "hourly": [
#                 {
#                     "chanceofrain": "60", 
#                     "precipMM": "1.2", 
#                     "windspeedKmph": "28", 
#                     "weatherDesc": [{"value": "Partly cloudy"}]
#                 }
#             ]
#         }]
#     }

#     async def run_normalization_test():
#         print("[*] Testing Tool 3 with mock raw API payload data...")
#         result = await normalize_weather_data_tool(mock_raw_api_data)
        
#         print(f"\n[+] Success Status: {result['success']}")
#         if result["success"]:
#             print(f"[+] Destination: {result['destination']} ({result['region']}, {result['country']})")
#             print(f"[+] Current Temperature (Type verified): {result['current_weather']['temperature_c']} (Type: {type(result['current_weather']['temperature_c']).__name__})")
#             print(f"[+] Max Chance of Rain calculated: {result['daily_forecast'][0]['max_chance_of_rain']}%")
#             print(f"[+] Total Precipitation calculated: {result['daily_forecast'][0]['total_precipitation_mm']} mm")
#         else:
#             print(f"[!] Normalization Crash: {result['message']}")

#     asyncio.run(run_normalization_test())
# Temporary manual validation engine for Tool 4 and Tool 5
# if __name__ == "__main__":
#     import asyncio
    
#     # 1. Mock normalized data matching Tool 3 output structure
#     mock_normalized_data = {
#         "destination": "Jaipur",
#         "region": "Rajasthan",
#         "country": "India",
#         "forecast_days": 1,
#         "current_weather": {
#             "temperature_c": 31.0,
#             "humidity": 48,
#             "precipitation_mm": 0.0,
#             "wind_speed_kmph": 12.0,
#             "weather_description": "Sunny"
#         },
#         "daily_forecast": [
#             {
#                 "date": "2026-06-26",
#                 "max_temp_c": 37.0,
#                 "min_temp_c": 27.0,
#                 "avg_temp_c": 32.0,
#                 "total_precipitation_mm": 1.2,
#                 "max_wind_kmph": 28.0,
#                 "max_chance_of_rain": 60,
#                 "weather_description": "Partly cloudy"
#             }
#         ]
#     }

#     async def run_risk_and_save_test():
#         print("[*] Testing Tool 4: Calculating weather risk indices...")
#         risk_result = await calculate_weather_risk_tool(mock_normalized_data)
        
#         print(f"[+] Risk Level Calculated: {risk_result['weather_risk']}")
#         # print(f"[+] Extracted Risk Factors: {risk_result['risk_factors']}")
#         # print(f"[+] Recommended Actions: {risk_result['recommended_actions']}")
        
#         # Assemble mock report structure
#         mock_final_report = {
#             **mock_normalized_data,
#             **risk_result,
#             "packing_suggestions": ["Water bottle", "Sunscreen"],
#             "travel_readiness_advisory": "Manageable with precautions.",
#             "weather_risk_explanation": "Medium due to high forecast temperatures."
#         }
        
#         print("\n[*] Testing Tool 5: Writing report document to disk...")
#         save_result = await save_travel_advisory_tool(mock_final_report)
        
#         print(f"[+] File Write Success: {save_result['success']}")
#         if save_result["success"]:
#             print(f"[+] Target Output Path Location: {save_result['saved_path']}")
#         else:
#             print(f"[!] Save Operation Encountered Failure: {save_result.get('message')}")

#     asyncio.run(run_risk_and_save_test())
