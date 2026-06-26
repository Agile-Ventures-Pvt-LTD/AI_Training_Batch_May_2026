# Weather and Travel Advisory MCP Server Using wttr.in API

# Project Overview

This project is designed especially on MCP Weather Travel Advisory which helps the user to understand the weather condition and based on this it will going to plan for future days. This will help the user very much so that user can be prevented from unwanted problems.

#  Project Objective
The objective of this project is to help participants understand how MCP servers 
expose:
1. Tools
2. Resources
3. Prompts

Participants must build an MCP server that can:

1. Accept a destination city.
2. Fetch weather data from wttr.in.
3. Normalize the weather response into a clean schema.
4. Calculate weather-based travel risk.
5. Use MCP resources for checklist, advisory rules, and forecast schema.
6. Use MCP prompts for travel readiness, risk explanation, and packing 
suggestions.
7. Save the final travel advisory report as JSON.

# Business Scenario
A traveler wants to check whether the weather is suitable for travel to a city.

Example questions:

Should I travel to Jaipur this weekend?

What should I pack for Pune based on the weather?

Is Mumbai risky for outdoor travel?

Can I travel comfortably to New Delhi over the next few days?

The MCP server should not behave like a generic weather chatbot. It should 
expose well-defined MCP tools, resources, and prompts so that an MCP
compatible client can use them in a structured way.

# Scope Boundary
This project is focused only on weather-based travel advisory.
The system should not handle:
- Flight booking
- Hotel booking
- Train booking
- Medical advice
- Disaster management alerts
- Visa rules
- Immigration rules
- Paid travel services

The final output should be treated as a simple weather-based travel advisory, not a 
guaranteed travel decision.

#  Required External API
Participants must use:

wttr.in JSON Weather API

No API key is required.

The API should be accessed using this pattern:

https://wttr.in/{city_name}?format=j1

Example:

https://wttr.in/Jaipur?format=j1

For city names with spaces, replace spaces with +.

Example:

https://wttr.in/New+Delhi?format=j1

Recommended fallback domain:

https://wttr.is/{city_name}?format=j1

Participants should use wttr.in as the primary domain and may use wttr.is as a 
fallback if the primary domain fails.

# API Usage Details
##  Request Method
Use HTTP GET.

Example using Python:

```python
import requests
city_name = "Jaipur"
url = f"https://wttr.in/{city_name}?format=j1"
response = requests.get(url, timeout=10)
data = response.json()
```

## Required API Endpoint

```python
GET https://wttr.in/{city_name}?format=j1

```

## Required Query Format
``` python
Scenario
Single-word city
City with space
Another city
Example URL
https://wttr.in/Jaipur?format=j1

https://wttr.in/New+Delhi?format=j1

https://wttr.in/Pune?format=j1
```

## Expected Raw API Sections

The wttr.in JSON response usually contains these top-level sections:
- current_condition
- nearest_area
- request
- weather

Participants do not need to use the complete raw response.
They should extract and normalize only the fields required by this PRD.

## Raw Fields to Use
From current_condition[0], use:
- temp_C
- humidity
- precipMM
- windspeedKmph
- weatherDesc

From nearest_area[0], use:
- areaName
- region
- country

From weather, use daily forecast fields such as:
- date
- maxtempC
- mintempC
- avgtempC
- totalSnow_cm
- hourly

From each day’s hourly list, participants should calculate or extract:
- chanceofrain
- precipMM
- windspeedKmph
- weatherDesc

##  Important Normalization Rule
Many values in the wttr.in JSON response are returned as strings.
Example:
```python
{
"temp_C": "31",
"humidity": "48",
"precipMM": "0.0",
"windspeedKmph": "12"
}
```

Participants must convert numeric strings to numbers before risk calculation.
Example:
```python
temperature_c = float(current["temp_C"])
humidity = int(current["humidity"])
precipitation_mm = float(current["precipMM"])
wind_speed_kmph = float(current["windspeedKmph"])
```

#  Required MCP Concepts
Participants must implement all three MCP primitives:
- MCP Tools
- MCP Resources
- MCP Prompts

For this project, their responsibilities are clearly separated.

# Important Implementation Clarifications
Participants must follow these rules to avoid overlap:
1. Only get_weather_forecast_tool should call the external wttr.in 
API.
2. MCP resources must be static reference content. They should not 
call APIs.
3. MCP prompts should only generate or guide natural-language text.
4. Risk calculation must be deterministic and implemented in 
calculate_weather_risk_tool.
5. The final report must not expose raw wttr.in JSON.
6. The final report must use the normalized schema defined in this 
PRD.

# Required MCP Tools
Participants must implement exactly these 5 mandatory MCP tools.
1. validate_city_input_tool
2. get_weather_forecast_tool
3. normalize_weather_data_tool
4. calculate_weather_risk_tool
5. save_travel_advisory_tool
Do not add additional mandatory tools in the base implementation.
Optional tools may be added only after the mandatory tools work.

## Tool 1: validate_city_input_tool
```python
Output
{
"success": true,
"original_city_name": "New Delhi",
"normalized_city_name": "New+Delhi"
}

Error Output
{
"success": false,
"message": "City name cannot be empty."}
```

##  Tool 2: get_weather_forecast_tool
```python
Output
{
"success": true,
"city_name": "Jaipur",
"raw_weather_data": {}
}

Error Output
{
"success": false,
"city_name": "InvalidCity",
"message": "Unable to fetch weather data."}
```

## Tool 3: normalize_weather_data_tool
```python
Normalized Output Schema
{
"success": true,
"destination": "Jaipur",
"region": "Rajasthan",
"country": "India",
"forecast_days": 3,
"current_weather": {
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
]}
```

## Tool 4: calculate_weather_risk_tool
Output
```python
{
"weather_risk": "MEDIUM",
"risk_factors": [
"Maximum temperature is expected to be above 35°C.",
"Chance of rain may increase during the forecast period."
],
"recommended_actions": [
"Carry water and avoid long outdoor exposure during afternoon 
hours.",
"Carry an umbrella or light rain protection."
]}
```

## Tool 5: save_travel_advisory_tool
```python
Output
{
"success": true,
"saved_path": "outputs/travel_advisory_report.json"
}
```

# Required MCP Resources

Participants must expose exactly these 3 MCP resources.
1. resource://travel/checklist
2. resource://travel/advisory-rules
3. resource://weather/normalized-forecast-schema

##  Resource 1: resource://travel/checklist
Purpose: 
Provides a static travel-readiness checklist.

Required Content: 

Travel Readiness Checklist:- Confirm destination and travel date.- Check weather forecast before departure.- Carry water during high-temperature conditions.- Carry umbrella or rain protection if rain risk exists.- Avoid unnecessary outdoor exposure during extreme heat.- Avoid exposed outdoor areas during high wind conditions.- Keep phone charged.- Carry essential documents.

## Resource 2: resource://travel/advisory-rules
Purpose:
Provides static rules for interpreting weather risk.

Required Content

Weather Advisory Rules:
- LOW:- No major heat, rain, or wind indicators.- Normal travel precautions are enough.
- MEDIUM:- Moderate heat, rain, or wind indicators exist.- Travel is possible, but the traveler should plan with basic precautions.
- HIGH:- High heat, high rain probability, heavy precipitation, or high wind 
condition exists.- The traveler should reconsider non-essential outdoor travel or plan 
with extra caution.

## Resource 3: resource://weather/normalized-forecast-schema
Purpose:

Describes the normalized forecast schema expected by this project.

Required Content
```python
{

"destination": "string",
"region": "string",
"country": "string",
"forecast_days": "number",
"current_weather": {
"temperature_c": "number",
"humidity": "number",
"precipitation_mm": "number",
"wind_speed_kmph": "number",
"weather_description": "string"
},
"daily_forecast": [
{
"date": "string",
"max_temp_c": "number",
"min_temp_c": "number",
"avg_temp_c": "number",
"total_precipitation_mm": "number",
"max_wind_kmph": "number",
"max_chance_of_rain": "number",
"weather_description": "string"
}
]
}
```

# Required MCP Prompts
Participants must expose exactly these 3 MCP prompts.
1. travel_readiness_prompt
2. weather_risk_summary_prompt
3. packing_recommendation_prompt
Prompts are reusable templates. They should not call APIs and should not perform 
deterministic risk calculation.

##  Prompt 1: travel_readiness_prompt

Purpose
Creates a concise travel-readiness advisory.
Inputs

```python
{
"destination": "Jaipur",
"weather_risk": "MEDIUM",
"forecast_summary": "",
"recommended_actions": []}
```
Prompt Template

```python
Create a concise travel-readiness advisory for the destination.
Destination: {destination}
Forecast Summary: {forecast_summary}
Weather Risk: {weather_risk}
Recommended Actions: {recommended_actions}
Explain whether travel looks comfortable, manageable with precautions, 
or risky due to weather.
Keep the answer practical and easy to understand.
```

##  Prompt 2: weather_risk_summary_prompt
Purpose
Explains why the risk level is LOW, MEDIUM, or HIGH.
Inputs
```python
{
"destination": "Jaipur",
"weather_risk": "MEDIUM",
"risk_factors": []
}
```
Prompt Template
Explain the weather risk level for the destination.
```python
Destination: {destination}
Risk Level: {weather_risk}
Risk Factors: {risk_factors}

```
Use simple language and explain the main reason behind the risk level.

##  Prompt 3: packing_recommendation_prompt
Inputs
```python
{
"destination": "Jaipur",
"weather_risk": "MEDIUM",
"risk_factors": []}

```
Prompt Template

Suggest practical packing items for the destination based on the 
weather risk.

```python
Destination: {destination}
Risk Level: {weather_risk}
Risk Factors: {risk_factors}
```

Return a short list of useful packing suggestions.


# Required Application Flow
Participants must implement the following flow.

User enters destination city

   ↓

MCP tool: validate_city_input_tool

   ↓

MCP tool: get_weather_forecast_tool

   ↓

MCP tool: normalize_weather_data_tool

   ↓

MCP resource: resource://weather/normalized-forecast-schema

   ↓

MCP tool: calculate_weather_risk_tool

   ↓

MCP resource: resource://travel/checklist

   ↓

MCP resource: resource://travel/advisory-rules

   ↓

MCP prompt: travel_readiness_prompt

   ↓

MCP prompt: weather_risk_summary_prompt

   ↓

MCP prompt: packing_recommendation_prompt

   ↓

MCP tool: save_travel_advisory_tool

   ↓

Final JSON advisory report


# Required Final Report Schema

The final report must be saved as:
```python
outputs/travel_advisory_report.json
```
The report must follow this schema:

```python
{
"destination": "",
"region": "",
"country": "",
"forecast_days": 3,
"current_weather": {
"temperature_c": 0,
"humidity": 0,
"precipitation_mm": 0,
"wind_speed_kmph": 0,
"weather_description": ""
},
"daily_forecast": [
{
"date": "",
"max_temp_c": 0,
"min_temp_c": 0,
"avg_temp_c": 0,
"total_precipitation_mm": 0,
"max_wind_kmph": 0,
"max_chance_of_rain": 0,
"weather_description": ""
}
],
"weather_risk": "LOW | MEDIUM | HIGH",
"risk_factors": [],
"recommended_actions": [],
"packing_suggestions": [],
"travel_readiness_advisory": "",
"weather_risk_explanation": "",
"resources_used": [
"resource://travel/checklist",
"resource://travel/advisory-rules",
"resource://weather/normalized-forecast-schema"
],
"tools_used": [
"validate_city_input_tool",
"get_weather_forecast_tool",
"normalize_weather_data_tool",
"calculate_weather_risk_tool",
"save_travel_advisory_tool"
],
"prompts_used": [
"travel_readiness_prompt",
"weather_risk_summary_prompt",
"packing_recommendation_prompt"
]
}

```

# Recommended Project Structure
```bash
p004_mcp_weather_travel_advisory/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── src/
│   ├── server.py
│   ├── tools.py
│   ├── resources.py
│   ├── prompts.py
│   ├── api_client.py
│   ├── schemas.py
│   └── report_writer.py
│
├── tests/
│   ├── test_api_client.py
│   ├── test_tools.py
│   ├── test_resources.py
│   ├── test_prompts.py
│   └── test_report_schema.py
│
├── outputs/
│   └── travel_advisory_report.json
│
└── sample_outputs/
    ├── sample_jaipur_advisory.json
    └── sample_pune_advisory.json
```

#  Required Python Packages
Minimum packages:
- mcp
- requests
- pydantic
- pytest
- python-dotenv

Optional packages:
- httpx
- rich
- pytest-mock

Participants may use either requests or httpx for API calls.

# Environment Variables
WTTR_PRIMARY_URL=https://wttr.in
WTTR_FALLBACK_URL=https://wttr.is
OUTPUT_PATH=outputs

# Setup
```python
uv venv

.venv\Scripts\activate

uv pip install -r requirements.txt

```

# API Client Requirements
``` python
import os
import requests
WTTR_PRIMARY_URL = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
WTTR_FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")
def get_weather_from_wttr(normalized_city_name: str) -> dict:
    urls = [
f"{WTTR_PRIMARY_URL}/{normalized_city_name}?format=j1",
f"{WTTR_FALLBACK_URL}/{normalized_city_name}?format=j1"
    ]
for url in urls:
try:
            response = requests.get(url, timeout=10)
if response.status_code == 200:
return {
"success": True,
"url_used": url,
"raw_weather_data": response.json()
                }
except Exception as error:
            last_error = str(error)
return {
"success": False,
"message": f"Unable to fetch weather data. Last error: 
{last_error}"
    }

```

# Required Commands
Install dependencies:
```python
pip install -r requirements.txt
```
Run MCP server:
```python
python src/server.py

```

Run tests:
```python
pytest tests/
```

Run integration tests:
```python
pytest -m integration
```

Optional sample command:
```python
python src/server.py --sample-city Jaipur
```

# API Testing
```python
import pytest
@pytest.mark.integration
def test_real_wttr_api_for_jaipur():
    ...
pytest tests/
pytest -m integration

```

# Expected Final Output Example
```python
{
"destination": "Jaipur",
"region": "Rajasthan",
"country": "India",
"forecast_days": 3,
"current_weather": {
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
],
"weather_risk": "MEDIUM",
"risk_factors": [
"Maximum temperature is expected to be above 35°C.",
"Wind speed may be moderately high during the forecast period."
],
"recommended_actions": [
"Carry water and avoid long outdoor exposure during afternoon 
hours.",
"Use sun protection if travelling outdoors."
],
"packing_suggestions": [
"Water bottle",
"Light cotton clothing",
"Sunscreen",
"Cap or hat"
],
"travel_readiness_advisory": "Travel appears manageable with basic 
weather precautions.",
"weather_risk_explanation": "The risk level is medium because 
moderate heat and wind indicators are present.",
"resources_used": [
"resource://travel/checklist",
"resource://travel/advisory-rules",
"resource://weather/normalized-forecast-schema"
],
"tools_used": [
"validate_city_input_tool",
"get_weather_forecast_tool",
"normalize_weather_data_tool",
"calculate_weather_risk_tool",
"save_travel_advisory_tool"
],
"prompts_used": [
"travel_readiness_prompt",
"weather_risk_summary_prompt",
"packing_recommendation_prompt"
]
}
```

#  Non-Functional Requirements
## NFR-1: Reliability
The system should handle:
1. Empty city name
2. City name with spaces
3. API timeout
4. API failure
5. Invalid JSON response
6. Missing expected fields
7. Missing output folder
8. Invalid final report schema


## NFR-2: Maintainability
The code should separate:
- MCP server setup
- Tools
- Resources
- Prompts
- API client
- Schemas
- Report writing
- Tests


## NFR-3: Output Quality
The final report should be:
- Structured
- Easy to understand
- Based on normalized weather data
- Saved as JSON
- Clear about risk level and recommended actions

# Author

## Vikash Kumar