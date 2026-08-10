# Weather Travel Advisory MCP

## 1. Project Overview
This project implements a Model Context Protocol (MCP) server that provides weather-based travel advisory for a city. It uses the wttr.in API to fetch weather data and generates a structured travel advisory report.

## 2. Business Use Case
A traveler can check whether weather conditions are suitable for travel.

Example queries:
- Should I travel to Jaipur this weekend?
- What should I pack for Pune?
- Is Mumbai risky for outdoor travel?

## 3. Technology Stack
- Python
- FastMCP
- Requests
- Pydantic
- Pytest
- python-dotenv

## 4. wttr.in API Usage
Endpoint:
https://wttr.in/{city}?format=j1

Example:
https://wttr.in/Jaipur?format=j1

- Uses HTTP GET
- No API key required
- Returns JSON response

## 5. MCP Tools
- validate_city_input_tool
- get_weather_forecast_tool
- normalize_weather_data_tool
- calculate_weather_risk_tool
- save_travel_advisory_tool

## 6. MCP Resources
- resource://travel/checklist
- resource://travel/advisory-rules
- resource://weather/normalized-forecast-schema

## 7. MCP Prompts
- travel_readiness_prompt
- weather_risk_summary_prompt
- packing_recommendation_prompt

## 8. Setup Instructions

1. Create virtual environment:
   uv venv

2. Activate environment:
   venv\Scripts\activate

3. Install dependencies:
   uv pip install -r requirements.txt

4. Create .env file:
   WTTR_PRIMARY_URL=https://wttr.in
   WTTR_FALLBACK_URL=https://wttr.is
   OUTPUT_PATH=outputs
   GROQ_API_KEY=....

## 9. How to Run the Application

python -m src.client

## 10. How to Run Tests

pytest tests/

If import errors:
python -m pytest -v tests/

## 11. How to Generate Sample Reports

Run the client:
python -m src.client

Use cities like Jaipur and Pune.

Copy file:
outputs/travel_advisory_report.json

Save into:
sample_outputs/sample_jaipur_advisory.json
sample_outputs/sample_pune_advisory.json

## 14. Final Report Schema

The report contains:
- destination, region, country
- current_weather
- daily_forecast
- weather_risk
- risk_factors
- recommended_actions
- packing_suggestions
- travel_readiness_advisory
- weather_risk_explanation
- resources_used
- tools_used
- prompts_used

## 15. Known Limitations
- Uses simple rule-based risk calculation
- City extraction is basic
- No advanced forecasting
- No UI

## 16. Future Improvements
- Better risk calculation logic
- Improved natural language understanding
- Support for multiple cities
- Add UI or dashboard
- Use LLM for enhanced responses