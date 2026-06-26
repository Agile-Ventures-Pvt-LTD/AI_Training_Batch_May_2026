# P004 Case Study 2: Weather and Travel Advisory MCP Server Using wttr.in API

An MCP (Model Context Protocol) server that uses the wttr.in weather API to fetch weather data for a city and generate a structured travel advisory report.

## Business Use Case

A traveler wants to check whether the weather is suitable for travel to a city. 
Example questions:
- Should I travel to Jaipur this weekend?
- What should I pack for Pune based on the weather?
- Is Mumbai risky for outdoor travel?
- Can I travel comfortably to New Delhi over the next few days?

## Technology Stack

- Python 3.10+
- MCP( model context protocol)
- wttr.in Weather API (no API key required)
- requests library for HTTP
- pydantic for data validation
- pytest for testing


## wttr.in API Usage

The server uses the wttr.in JSON API:
```
https://wttr.in/{city_name}?format=j1
```

For cities with spaces, replace spaces with +:
```
https://wttr.in/New+Delhi?format=j1
```

### Fallback Domain
If wttr.in is unavailable, the server automatically falls back to:
```
https://wttr.is/{city_name}?format=j1
```

### API Response Sections Used
- `current_condition[0]`: temp_C, humidity, precipMM, windspeedKmph, weatherDesc
- `nearest_area[0]`: areaName, region, country
- `weather`: date, maxtempC, mintempC, avgtempC, hourly data (windspeedKmph, chanceofrain, precipMM, weatherDesc)

## MCP Tools 


1. validate_city_input: Validates city name, strips spaces replaces internal spaces 
2. get_weather_forecast : Calls wttr.in JSON API and returns raw weather response 
3. normalize_weather_data : Converts raw wttr.in JSON into clean internal weather schema 
4. calculate_weather_risk : Calculates deterministic travel weather risk (LOW/MEDIUM/HIGH) 
5. Save_travel_advisory: Saves the final advisory report as JSON 


## MCP Resources 

1. resource://travel/checklist : Static travel-readiness checklist
2. resource://travel/advisory-rules : Static rules for interpreting weather risk 
3. resource://weather/normalized-forecast-schema : Describes the normalized forecast schema 

## MCP Prompts 


1. travel_readiness_prompt : Creates a concise travel-readiness advisory 
2. weather_risk_summary_prompt: Explains why the risk level is LOW, MEDIUM, or HIGH 
3. packing_recommendation_prompt : Generates practical packing suggestions 

## Setup Instructions

1. *** Folder Structure ***:
 ```
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

2. Create a virtual environment 
```bash
uv venv
 .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. make .env
```bash
   WTTR_PRIMARY_URL=https://wttr.in
   WTTR_FALLBACK_URL=https://wttr.is
   OUTPUT_PATH=outputs
```

## How to Run the MCP Server

### Standard mode (stdio transport):
```bash
python src/server.py
```

### Generate a sample report for a city:
```bash
python src/server.py --sample-city Jaipur
python src/server.py --sample-city Pune
python src/server.py --sample-city "New Delhi"
```

## How to Run Tests

### Run all unit tests:
```bash
pytest tests/
```

### Run integration tests (requires internet access):
```bash
pytest -m integration tests/
```

### Run tests with verbose output:
```bash
pytest -v tests/
```

## How to Generate Sample Reports

To generate sample advisory reports for the required cities:

```bash
python src/server.py --sample-city Jaipur
python src/server.py --sample-city Pune
```

Reports are saved to `outputs/travel_advisory_report.json`.

Sample outputs are also provided in the `sample_outputs/` directory.

## Final Report Schema

```json
{
  "destination": "string",
  "region": "string",
  "country": "string",
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
  "resources_used": [],
  "tools_used": [],
  "prompts_used": []
}
```

## Risk Calculation Rules

```
max_temp_c >= 40   --->    High heat risk
35 <= max_temp_c < 40  --->  Moderate heat risk
total_precipitation_mm >= 20  ---->   High rain risk
5 <= total_precipitation_mm < 20  --->  Moderate rain risk
max_chance_of_rain >= 70  --->  High rain probability
40 <= max_chance_of_rain < 70  --->  Moderate rain probability
max_wind_kmph >= 40 --->  High wind risk
25 <= max_wind_kmph < 40 --->   Moderate wind risk

```
*** Overall Risk Logic ***

1. High : Any high-risk condition exists.
2. Medium : No high-risk condition exists, but at least one moderate-risk condition exists.
3. Low : No high-risk or moderate-risk condition exists.


## Known Limitations

1. The wttr.in API may occasionally be slow or unavailable. A fallback domain (wttr.is) is used but may also be unavailable.
2. The risk calculation is deterministic and does not consider real-time weather alerts or warnings.


## Future Improvements

1. Implement  a web interface or ClI interacting mode for easier usage 
2. Add more granular risk factors such as humidity comfort levels and UV index.
