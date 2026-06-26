#  P004 Case Study 2: Weather and Travel Advisory MCP Server

A production-ready Model Context Protocol (MCP) server engineered to provide automated, weather-driven travel advisories utilizing the public wttr.in JSON API. The server seamlessly exposes 5 diagnostic tools, 3 static architectural resources, and 3 contextual prompt templates to any MCP-compliant client environment (such as Claude Desktop).

------------------------------
##  Project Overview
This server functions as a centralized intelligence engine for travel risk mitigation. By integrating directly into an LLM client's toolkit via standard input/output streams (stdio), it transforms raw, unstructured data feeds into standardized, metric-validated travel advisory JSON reports.
##  Example Business Use Cases

*  Assessing Destination Safety: "Should I travel to Jaipur this weekend?"
*  Automating Smart Logistics: "What should I pack for Pune based on the weather?"
*  Risk Mitigation Evaluation: "Is Mumbai risky for outdoor travel?"

------------------------------
##  Project Structure
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
------------------------------
#  Tech Stack

* Server Framework: mcp Python SDK (FastMCP)
* HTTP Network Client: requests
* Data Schema Validation Layer: pydantic
* Testing Environment: pytest & pytest-mock
* Environment Configuration: python-dotenv
* Runtime Language: Python 3.10+

------------------------------
#  Environment Variables & Setup
## 1. Initialize Workspace
Clone or navigate to the project directory, then instantiate an isolated virtual environment:
```
python -m venv 
```
## Activate on Linux/Mac
```
source venv/bin/activate 
``` 
## Activate on Windows
```
venv\Scripts\activate
```   

## 2. Install Package Matrix
Install all mandatory platform dependencies defined in the core manifest file:
```
pip install -r requirements.txt
```

## 3. Apply Environment Keys
Copy the baseline template configuration to instantiate your active environmental state:
```
cp .env.example .env
```

Default environment parameters inside .env:
```
WTTR_PRIMARY_URL=https://wttr.in
WTTR_FALLBACK_URL=https://wttr.is
OUTPUT_PATH=outputs
```

------------------------------
#  MCP System Specification
##  1. MCP Tools (5 Mandatory Nodes)
The server exposes 5 programmatic tools executing strict functional domains:
   1. validate_city_input_tool: Validates the incoming city text string and sanitizes white spaces into API-compatible + formats.
   2. get_weather_forecast_tool: The exclusive gateway node responsible for executing remote network requests against the weather APIs.
   3. normalize_weather_data_tool: Safe parsing engine transforming raw, nested JSON payloads into predictable, numeric structures.
   4. calculate_weather_risk_tool: A completely deterministic logic processor mapping parameters against fixed safety thresholds without any LLM halluncination risks.
   5. save_travel_advisory_tool: File I/O manager committing finalized report metrics directly onto standard storage arrays.

##  2. MCP Resources (3 Static Contexts)
Exposes architectural files and references directly to the consuming model:

   1. resource://travel/checklist: Standard procedural travel-readiness checks.
   2. resource://travel/advisory-rules: Domain logic explaining criteria bounds for LOW, MEDIUM, and HIGH hazard groups.
   3. resource://weather/normalized-forecast-schema: Machine-readable target JSON format blueprint documentation.

##  3. MCP Prompts (3 Template Layouts)
Provides structured, parameter-ready prompt skeletons to orchestrating client LLMs:

   1. travel_readiness_prompt: Template compiling safety status summaries into localized situational advice.
   2. weather_risk_summary_prompt: Template mapping hazard points into clear, human-readable risk summaries.
   3. packing_recommendation_prompt: Template matching forecasted temperature and rain vectors with specific luggage suggestions.

------------------------------
##  Execution & Operation Manual## Launching the Production Stream
Start the application using the standard stdio transport system. This endpoint is built to connect natively with orchestrators like Claude Desktop:
```
python src/server.py
```

## Locally Generating Sample Reports (CLI Mode)
You can bypass network orchestrators entirely to execute the localized parsing stream on demand using the **--sample-city** CLI argument. This processes 3 days of forecast data and outputs the final result into the outputs/ folder:

## Process report for Jaipur
```
python src/server.py --sample-city Jaipur
```
## Process report for Pune
```
python src/server.py --sample-city Pune
```
## Process report for New Delhi (Handles automatic space-to-plus normalization)
```
python src/server.py --sample-city "New Delhi"
```

------------------------------
##  Final Report Output Schema
The artifact produced by both the automated tools and CLI workflows maps strictly to the following validation schema:
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
    "weather_description": "string"
  },
  "daily_forecast": [
    {
      "date": "string",
      "max_temp_c": 0.0,
      "min_temp_c": 0.0,
      "avg_temp_c": 0.0,
      "total_precipitation_mm": 0.0,
      "max_wind_kmph": 0.0,
      "max_chance_of_rain": 0,
      "weather_description": "string"
    }
  ],
  "weather_risk": "LOW | MEDIUM | HIGH",
  "risk_factors": [ "string" ],
  "recommended_actions": [ "string" ],
  "packing_suggestions": [ "string" ],
  "travel_readiness_advisory": "string",
  "weather_risk_explanation": "string",
  "resources_used": [ "string" ],
  "tools_used": [ "string" ],
  "prompts_used": [ "string" ]
}
```
------------------------------
##  Quality Testing & Verification Matrix
The pipeline splits testing domains into offline unit tests and live network checks:
## 1. Isolated Offline Unit Testing
Runs 29 tests verifying local calculations, input sanitization routines, static resources, and Pydantic validation boundaries using API mocking:
```
pytest tests/ -v
```
### Expected Output
```shell
collected 29 items                                                                   

tests/test_api_client.py::test_api_client_success PASSED
tests/test_api_client.py::test_api_client_http_error PASSED
tests/test_api_client.py::test_api_client_timeout PASSED
tests/test_api_client.py::test_api_client_connection_error PASSED
tests/test_prompts.py::test_required_prompts_available PASSED
tests/test_prompts.py::test_travel_readiness_prompt_content PASSED
tests/test_prompts.py::test_weather_risk_summary_prompt_content PASSED
tests/test_prompts.py::test_packing_recommendation_prompt_content PASSED
tests/test_report_schema.py::test_final_report_schema_valid ERROR
tests/test_report_schema.py::test_report_serializable_to_json ERROR
tests/test_resources.py::test_required_resources_available PASSED
tests/test_resources.py::test_travel_checklist_content PASSED
tests/test_resources.py::test_advisory_rules_content PASSED
tests/test_resources.py::test_normalized_forecast_schema_content PASSED
tests/test_tools.py::test_validate_city_input_tool_valid_city PASSED
tests/test_tools.py::test_validate_city_input_tool_city_with_space PASSED
tests/test_tools.py::test_validate_city_input_tool_empty_city PASSED
tests/test_tools.py::test_validate_city_input_tool_whitespace_only PASSED
tests/test_tools.py::test_validate_city_input_tool_short_city PASSED
tests/test_tools.py::test_get_weather_forecast_tool_mock_success ERROR
tests/test_tools.py::test_get_weather_forecast_tool_mock_failure PASSED
tests/test_tools.py::test_normalize_weather_data_tool_schema ERROR
tests/test_tools.py::test_normalize_weather_data_tool_empty_input PASSED
tests/test_tools.py::test_calculate_weather_risk_tool_valid_risk_level ERROR
tests/test_tools.py::test_calculate_weather_risk_tool_high_heat PASSED
tests/test_tools.py::test_calculate_weather_risk_tool_moderate_heat PASSED
tests/test_tools.py::test_calculate_weather_risk_tool_low PASSED
tests/test_tools.py::test_save_travel_advisory_tool PASSED
tests/test_tools.py::test_real_wttr_api_for_jaipur PASSED 
```

## 2. Live API Integration Tests
Executes real network queries against wttr.in endpoints to verify live end-to-end connectivity:
```
pytest -m integration -v
```
### Expected Output
```shell
collected 29 items / 28 deselected / 1 selected
tests/test_tools.py::test_real_wttr_api_for_jaipur PASSED 
```
------------------------------
##  Known Limitations

* Upstream Dependability: Weather diagnostic data accuracy is fully dependent on the operational status of the public wttr.in server array.
* Threshold Rigidness: The risk assessment engine runs on strict, deterministic numerical cutoffs, without cross-referencing variable metadata like UV Indexes or Relative Humidity indices.
* Template Generation: When running locally via CLI, prompts use fallback templates rather than active LLM processing layers.
* Transport Restrictions: The pipeline is built exclusively on top of stdio standard streams (HTTP/SSE transport models are not supported).
* Temporal Boundaries: Limit thresholds restrict data compilation to exactly a 3-day forecast window.

------------------------------
##  Future Improvements Roadmap

*  Enhanced Risk Grading: Incorporate humidity metrics and UV indexes to compute a more accurate apparent comfort factor.
*  Expanded Transport Layer: Implement full HTTP and Server-Sent Events (SSE) interfaces to support web-integrated enterprise clients.
*  Native LLM Layer Integration: Wire deep semantic generation models directly into the pipeline for fluid, natural-language advisory output notes.
*  Smart Persistence Caching: Add an optimized local persistence layer (SQLite/Redis) to minimize outbound queries and avoid upstream rate limits.
*  Extended Forecasting: Support 7+ day windows when extended telemetry feeds are present.

------------------------------
## 🧑‍💻 Author
Pranay Gupta


