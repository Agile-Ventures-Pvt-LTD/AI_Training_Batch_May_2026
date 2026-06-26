# P004 Case Study 2: Weather and Travel Advisory MCP Server Using wttr.in API

## 1. Project Overview
This project implements a Model Context Protocol (MCP) server that provides weather-based travel advisory tools, resources, and prompts. It accepts a destination city, retrieves weather forecasts from the public `wttr.in` JSON API, normalizes the data, determines potential weather-related travel risks, and generates a structured JSON travel advisory report.

## 2. Business Use Case
Travelers frequently need to know whether current or upcoming weather makes travel to a specific city comfortable or risky. This server exposes well-defined tools, resources, and prompts so that an MCP-compatible client (such as a developer environment or AI agent) can retrieve and structure advisories for questions like:
- "Should I travel to Jaipur this weekend?"
- "What should I pack for Pune based on the weather?"
- "Is Mumbai risky for outdoor travel?"

## 3. Technology Stack
- **Python**: >= 3.13
- **FastMCP**: Python SDK for Model Context Protocol
- **Requests**: HTTP client for API fetches
- **Pydantic**: Data validation and schema enforcement
- **Pytest**: Test runner for unit and integration tests

## 4. wttr.in API Usage Details
This project communicates with `wttr.in` via standard HTTP GET requests:
- **Primary Endpoint**: `https://wttr.in/{city_name}?format=j1`
- **Fallback Endpoint**: `https://wttr.is/{city_name}?format=j1`
- **Spaces in City Names**: Internal spaces are normalized to `+` (e.g., `New+Delhi`).
- **Timeout**: Requests have a deterministic 10-second timeout.
- **Failures**: Unreachable hosts or malformed JSON return structured errors without crashing.

## 5. MCP Tools List
The server exposes exactly 5 mandatory tools:
1. `validate_city_input_tool(city_name: str)`: Cleans and validates city names.
2. `get_weather_forecast_tool(normalized_city_name: str)`: Fetches raw JSON weather data from the external API.
3. `normalize_weather_data_tool(raw_weather_data: dict)`: Normalizes raw response into a clean schema.
4. `calculate_weather_risk_tool(normalized_weather_data: dict)`: Computes deterministic travel risk (LOW, MEDIUM, HIGH) based on temperature, rain probability, precipitation, and wind speed.
5. `save_travel_advisory_tool(report: dict)`: Saves the generated report to `outputs/travel_advisory_report.json`.

## 6. MCP Resources List
Exposed under standard URIs:
1. `resource://travel/checklist`: Provides static travel-readiness checklist.
2. `resource://travel/advisory-rules`: Rules for interpreting LOW, MEDIUM, and HIGH weather risks.
3. `resource://weather/normalized-forecast-schema`: The JSON schema defining normalized forecasts.

## 7. MCP Prompts List
Templates that help clients construct natural language advice:
1. `travel_readiness_prompt`: Creates a concise travel-readiness summary.
2. `weather_risk_summary_prompt`: Explains why the risk level is LOW, MEDIUM, or HIGH.
3. `packing_recommendation_prompt`: Generates packing lists based on weather conditions.

## 8. Setup Instructions
To run this project, make sure Python and `uv` (or `pip`) are installed:

1. Clone or navigate to the project directory:
   ```bash
   cd mcp_weather_travel_advisory
   ```
2. Create and activate a virtual environment, then install dependencies:
   ```bash
   uv sync
   # OR using pip:
   pip install -r requirements.txt
   ```
3. Create a `.env` file from the example:
   ```bash
   copy .env.example .env
   ```

## 9. How to Run the MCP Server
Launch the MCP server locally over standard I/O (stdio) using:
```bash
uv run python -m src.server
# OR
python src/server.py
```

## 10. How to Run Tests
Run the unit test suite (using mocked wttr.in responses to avoid making network requests):
```bash
uv run pytest
```

## 11. How to Run Integration Tests
To run tests that perform actual network requests against the real `wttr.in` endpoints:
```bash
uv run pytest -m integration
```

## 12. How to Generate Sample Reports
Run the sample execution flow for a specific city. This simulates the client flow, calling all tools sequentially, and saving a report to `outputs/travel_advisory_report.json`:
```bash
uv run python -m src.server --sample-city Jaipur
# OR
uv run python -m src.server --sample-city Pune
```

## 13. Final Report Schema
Generated reports saved to `outputs/travel_advisory_report.json` conform to:
```json
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
```

## 14. Known Limitations
- **wttr.in Rate Limits**: The public API might return HTTP 503 or 429 during high volume.
- **Geocoding Dependency**: If wttr.in fails to map a name to a valid location, the parser cannot extract country or region information and will return a normalization failure.
- **Deterministic Risk Model**: The current risk analysis model evaluates simple thresholds (e.g. max temperature or wind speed) and does not adapt to season or region-specific baselines.

## 15. Future Improvements
- **Caching Layer**: Store API weather responses locally for 10-15 minutes to reduce external network traffic.
- **Improved Fallback API**: Integrate secondary weather APIs (e.g., Open-Meteo or weatherapi.com) with API key authorization if wttr.in goes down.
- **Interactive Prompts**: Integrate a LLM wrapper directly inside the sample client code to query prompts and generate the advisory/recommendation texts dynamically rather than using template strings.
