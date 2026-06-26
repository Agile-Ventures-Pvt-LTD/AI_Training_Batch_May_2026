# Weather and Travel Advisory MCP Server Using wttr.in API

## Project overview
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

## Business use case
A traveler wants to check whether the weather is suitable for travel to a city.
Example questions:
- Should I travel to Jaipur this weekend?
- What should I pack for Pune based on the weather?
- Is Mumbai risky for outdoor travel?
- Can I travel comfortably to New Delhi over the next few days?
The MCP server should not behave like a generic weather chatbot. It should 
expose well-defined MCP tools, resources, and prompts so that an MCPcompatible client can use them in a structured way


## Technology stack
mcp
requests
pydantic
pytest
python-dotenv
httpx
rich
pytest-mock

## wttr.in API usage details

## MCP tools list
1.  validate_city_input_tool (Validates the city name entered by the user)
2. get_weather_forecast_tool (Calls the wttr.in JSON API and returns the raw weather response.)
3. normalize_weather_data_tool (Converts raw wttr.in JSON into a clean internal weather schema.)
4. calculate_weather_risk_tool (Calculates deterministic travel weather risk from normalized weather data.)
5. save_travel_advisory_tool (Saves the final advisory report as JSON.)

## MCP resources list
1. resource://travel/checklist (Provides a static travel-readiness checklist)
2. resource://travel/advisory-rules (Provides static rules for interpreting weather risk)
3. resource://weather/normalized-forecast-schema (Describes the normalized forecast schema expected by this project.)

## MCP prompts list
1. travel_readiness_prompt (Creates a concise travel-readiness advisory.)
2. weather_risk_summary_prompt (Explains why the risk level is LOW, MEDIUM, or HIGH)
3. packing_recommendation_prompt (Generates practical packing suggestions.)

## Setup instructions
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

## How to run the MCP server

run python/src/server.py

## How to run tests
run pytest tests/

## How to run integration tests
run pytest -m integration

## How to generate sample reports
run python src/client.py Jaipur

## Final report schema
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

## Known limitations

## Future improvements
