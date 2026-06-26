# Travel Weather Advisory MCP
This project provides an MCP server to check weather conditions and generate travel advisories using wttr.in.

# Business use case
A traveler wants to check whether the weather is suitable for travel to a city and get a structured JSON advisory report.

# Tech stack
```text
Python, FastMCP, wttr.in API, Pytest
```
# wttr.in API usage details

```bash
Endpoint: GET https://wttr.in/{city_name}?format=j1Spaces
```
in city names spaces are replaced with + (example: New+Delhi).
---

# Folder Structure

```text
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
|   |-- client.py
│   └── report_writer.py
│
├── tests/
│   ├── test_api_client.py
│   ├── test_tools.py
│   ├── test_resources.py
│   ├── test_prompts.py
|   |-- test_client.py
│   └── test_report_schema.py
│
├── outputs/
│   └── travel_advisory_report.json
│
└── sample_outputs/
    ├── sample_jaipur_advisory.json
    └── sample_pune_advisory.json
```
---

# MCP tools list

- validate_city_input_tool
- get_weather_forecast_tool
- normalize_weather_data_tool
- calculate_weather_risk_tool
- save_travel_advisory_tool
---

# MCP resources list
- resource://travel/checklist
- resource://travel/advisory-rules
- resource://weather/normalized-forecast-schema
---

# MCP prompts list

- travel_readiness_prompt
- weather_risk_summary_prompt
- packing_recommendation_prompt
---

# Requirements
```txt
requirements.txt file
fastmcp
requests
python-dotenv
langchain-groq
mcp-use
pytest
```
---
# Setup instructions
Create a virtual environment 
```bash
uv venv or uv inint
```
and install dependencies: 

```bash
uv pip install -r requirements.txt
or
uv add requirements.txt if (uv init)
Copy .env.example to .env and add your GROQ_API_KEY.
```
# How to run the MCP server 
- NOTE (We are Running the server with the STDIO)
Run the server using the mcp.json configuration via the client.

# How to run tests
```bash
pytest tests/
```
# How to run integration tests
```bash
pytest -m integration
```

# Final report schema
The final report follows the schema defined in src/schemas.py (get_final_report_schema).

# Known limitations
Risk calculation is deterministic and relies strictly on the defined values.

# Future improvements
Add historical weather data comparison.