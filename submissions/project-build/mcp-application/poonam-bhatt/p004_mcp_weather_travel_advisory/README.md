# Weather and Travel Advisery MCP Server Using wttr.in API

This is a Model Context Protocol (MCP) server that connects AI models to the public wttr.in JSON API to generate weather-based travel advisory reports. It implements MCP tools, resources, and prompts, enabling an MCP-compatible client (like Claude Desktop) to request a city, check weather conditions, evaluate risks, pack appropriately, and save structured travel reports.

## 1. Project Overview

This project provides a structured, weather-based travel advisory using the Model Context Protocol. It accepts destination input, fetches current conditions and 3-day forecasts, calculates travel risks based on heat, rain, and wind metrics, and outputs a normalized JSON travel advisory report.

## 2. Business Use Case

Travelers often ask open-ended questions like:

"Should I travel to Jaipur this weekend?"
"What should I pack for Pune based on the weather?"
"Is Mumbai risky for outdoor travel?"
Instead of acting as a generic chatbot, this server offers tools, schemas, and prompts to make these decisions structured, deterministic, and repeatable.

## 3. Technology Stack

Language: Python 3.10+
Protocol: Model Context Protocol (MCP) via the Python mcp SDK (FastMCP)
API Client: requests for fetching data from wttr.in
Validation: pydantic (v2) for strict schema compliance
Configuration: python-dotenv
Testing: pytest, pytest-mock

## 4. wttr.in API Usage Details

The server queries the wttr.in JSON API. No API key is required.

Endpoint: https://wttr.in/{city_name}?format=j1
Fallback URL: https://wttr.is/{city_name}?format=j1
Behavior: Spaces in city names are converted to + (e.g. New+Delhi). The client tries the primary URL first and uses the fallback if the primary fails.

## 5. MCP Primitives Exposed

MCP Tools List
validate_city_input_tool
Validates that the city name is not empty, is at least 2 characters, strips whitespace, and replaces spaces with +.
get_weather_forecast_tool
Queries wttr.in or wttr.is and returns the raw weather JSON.
normalize_weather_data_tool
Converts raw wttr.in JSON data into a clean internal weather schema, parsing strings to floats/ints.
calculate_weather_risk_tool
Evaluates risk deterministically (LOW, MEDIUM, HIGH) using rules for max temperature, total precipitation, chance of rain, and max wind speed.
save_travel_advisory_tool
Writes the completed travel advisory report to outputs/travel_advisory_report.json.
MCP Resources List
resource://travel/checklist
Provides a static travel-readiness checklist.
resource://travel/advisory-rules
Provides static guidelines for interpreting weather risk.
resource://weather/normalized-forecast-schema
Exposes the expected Pydantic schema for normalized forecast outputs.
MCP Prompts List
travel_readiness_prompt
Template guiding the creation of a concise travel-readiness advisory.
weather_risk_summary_prompt
Template for explaining the reasons behind the risk level.
packing_recommendation_prompt
Template for generating packing suggestions.


## 6. Setup Instructions
Clone or Navigate to the Directory:

bash

cd C:\Users\Poonam Bhatt\.gemini\antigravity\scratch\p004_mcp_weather_travel_advisory
Create a Virtual Environment & Activate it:

bash

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate
Install Dependencies:

bash

pip install -r requirements.txt
Initialize Environment Variables: Copy the example environment variables:

bash

cp .env.example .env


## 7. Execution Guide
How to Run the MCP Server
Launch the server using stdio transport:

bash

python src/server.py
How to Generate Sample Reports (Offline Pipeline)
We have included a pipeline simulation command to run the complete flow for a city, fetch live API data, calculate risks, generate advisory texts, and save the reports:

bash

# Generate report for Jaipur
python src/server.py --sample-city Jaipur
# Generate report for Pune
python src/server.py --sample-city Pune
These commands write reports to:

outputs/travel_advisory_report.json
sample_outputs/sample_jaipur_advisory.json (or sample_pune_advisory.json)



## 8. Folder Structure

p004_mcp_weather_travel_advisory/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── src/
│ ├── server.py
│ ├── tools.py
│ ├── resources.py
│ ├── prompts.py
│ ├── api_client.py
│ ├── schemas.py
│ └── report_writer.py
│
├── tests/
│ ├── test_api_client.py
│ ├── test_tools.py
│ ├── test_resources.py
│ ├── test_prompts.py
│ └── test_report_schema.py
│
├── outputs/
│ └── travel_advisory_report.json
│
└── sample_outputs/
 ├── sample_jaipur_advisory.json
 └── sample_pune_advisory.json


## 9. Testing Guide
How to Run Unit Tests
To run the offline unit test suite (utilizing mocks):

bash

pytest tests/
How to Run Integration Tests
To test actual connectivity to the wttr.in API:

bash

pytest -m integration


## 10. Final Report Schema
Reports saved to outputs/travel_advisory_report.json conform to this schema:

json

{
  "destination": "string",
  "region": "string",
  "country": "string",
  "forecast_days": "integer",
  "current_weather": {
    "temperature_c": "number",
    "humidity": "integer",
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
  ],
  "weather_risk": "LOW | MEDIUM | HIGH",
  "risk_factors": ["string"],
  "recommended_actions": ["string"],
  "packing_suggestions": ["string"],
  "travel_readiness_advisory": "string",
  "weather_risk_explanation": "string",
  "resources_used": ["string"],
  "tools_used": ["string"],
  "prompts_used": ["string"]
}


## 11. OUTPUTS :

## 11(a) pytest run

command - uv run pytest
================================== test session starts ============================================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Poonam Bhatt\Desktop\project_build_04\p004_mcp_weather_travel_advisory
configfile: pyproject.toml
plugins: anyio-4.14.1, mock-3.15.1
collected 12 items                                                                                                       

tests\test_api_client.py...                                                                  [25%]
tests\test_prompts.py  .                                                                     [33%]
tests\test_report_schema.py  .                                                               [41%]
tests\test_resources.py     .                                                                [50%]
tests\test_tools.py ......                                                                   [100%]

======================================== 12 passed in 1.89s ========================================

## 11(b) Server run

command - python -m src.server --sample-city Jaipur

=== Running Travel Advisory Pipeline for: Jaipur ===

[Step 1] Validating city input...
-> Normalized city: Jaipur

[Step 2] Fetching raw weather forecast from wttr.in...
-> Weather data retrieved successfully.

[Step 3] Normalizing weather data...
-> Normalization succeeded.

[Step 4] Calculating weather risk...
-> Risk Level: HIGH
-> Risk Factors: ['Extreme heat risk: Maximum temperature is expected to reach 40°C or above.', 'Wind speed may be moderately high during the forecast period.']
-> Recommended Actions: ['Avoid outdoor exposure during peak afternoon hours and stay hydrated.', 'Use caution if travelling outdoors.']

[Step 5] Accessing static resources...
-> Read checklist, advisory rules, and normalized forecast schema.

[Step 6] Simulating LLM prompts output...
-> Advisory: Travel to Jaipur is currently risky due to severe weather conditions. Non-essential outdoor activities should be reconsidered or planned with extreme caution.
-> Explanation: The risk level is high because of: Extreme heat risk: Maximum temperature is expected to reach 40°C or above. and Wind speed may be moderately high during the forecast period.. These conditions may impact outdoor safety and transit.
-> Packing Suggestions: ['Standard clothing', 'Mobile charger', 'Personal toiletries', 'First-aid kit', 'Water bottle', 'Light cotton clothing']

[Step 7] Assembling final travel advisory report...

[Step 8] Saving report...
-> Saved report to: outputs/travel_advisory_report.json
-> Saved sample output copy to: sample_outputs/sample_jaipur_advisory.json

=== Success! Pipeline finished ===



## 12. Known Limitations
API Rate Limiting: The public wttr.in endpoint can sometimes be rate-limited or return 503 during high traffic.
Text Simulation: When run offline, LLM prompt responses are simulated using deterministic rules rather than generated by a neural model.
No Historical Data: The server only provides short-term forecasts (up to 3 days) and cannot analyze seasonal trends.


## 12. Future Improvements
Advanced Fallbacks: Integrate secondary weather API clients (e.g. Open-Meteo) as fallbacks when both wttr.in and wttr.is are offline.
Dynamic Checklists: Customize the travel readiness checklist dynamically based on the risk factors rather than returning static resources.
Caching: Implement response caching (e.g. SQLite or Redis) to minimize API requests wit