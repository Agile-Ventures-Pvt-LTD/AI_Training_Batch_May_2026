# Weather and Travel Advisory MCP Server Using wttr.in API
This project is focused only on weather-based travel advisory.

# 1. Business Scenario
- A traveler wants to check whether the weather is suitable for travel to a city.
- Example questions:
1. Should I travel to Jaipur this weekend?
2. What should I pack for Pune based on the weather?
3. Is Mumbai risky for outdoor travel?
4. Can I travel comfortably to New Delhi over the next few days?
- The MCP server should not behave like a generic weather chatbot. It should 
- expose well-defined MCP tools, resources, and prompts so that an MCP compatible client can use them in a structured way.

## 2. Technology Stack
fastmcp>=3.1.0
ipython>=9.10.0
requests>=2.32.5
python-dotenv>=1.2.2
mcp-use>=1.6.0
langchain-groq>=1.1.2
pypdf>=6.7.5
pydantic-ai>=1.78.0
pytest
---

## 4. wttr.in API Usage Details
The implementation interfaces with upstream JSON query layers provided by `wttr.in`:
*   **Primary Destination Target:** `https://wttr.in{normalized_city_name}?format=j1`
*   **Secondary Resiliency Target:** `https://wttr.is{normalized_city_name}?format=j1`
---

## 5. MCP Tools List
*  validate_city_input_tool
*  get_weather_forecast_tool
*  normalize_weather_data_tool
*  calculate_weather_risk_tool
*  save_travel_advisory_tool
---

## 6. MCP Resources List
*   resource://travel/checklist
*   resource://travel/advisory-rules
*   resource://weather/normalized-forecast-schema
---

## 7. MCP Prompts List
*   travel_readiness_prompt
*   weather_risk_summary_prompt
*   packing_recommendation_prompt
---

## 8. Setup Instructions

1. Initialize and configure your virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1   # Windows PowerShell
  
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 9. How to Run the MCP Server
```bash
python src/server.py 
```

---

## 10. How to Run Tests

```bash
python -m pytest
```
---


## 12. How to Generate Sample Reports
```bash
python src/server.py --sample-city "New Delhi"
```
The output will save in this file `outputs/travel_advisory_report.json` in json format.

---

## 13. Final Report Schema
The output saved by the system conforms exactly to this structured schema layout:

```json
{
  "destination": "string",
  "region": "string",
  "country": "string",
  "forecast_days": "integer",
  "current_weather": {
    "temperature_c": "float",
    "humidity": "integer",
    "precipitation_mm": "float",
    "wind_speed_kmph": "float",
    "weather_description": "string"
  },
  "daily_forecast": [
    {
      "date": "string",
      "max_temp_c": "float",
      "min_temp_c": "float",
      "avg_temp_c": "float",
      "total_precipitation_mm": "float",
      "max_wind_kmph": "float",
      "max_chance_of_rain": "integer",
      "weather_description": "string"
    }
  ],
  "weather_risk": "string (LOW | MEDIUM | HIGH)",
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

---

## 14. Known Limitations
*   Upstream Rate Limits Because the `wttr.in` endpoints are open-access public layers, they can occasionally return HTTP `429 Too Many Requests` codes during high-volume periods.

## 15. Future Improvements
* Asynchronous Processing Re-architect network requests using `httpx` and `asyncio` to handle simultaneous multi-destination travel tracking effectively.
