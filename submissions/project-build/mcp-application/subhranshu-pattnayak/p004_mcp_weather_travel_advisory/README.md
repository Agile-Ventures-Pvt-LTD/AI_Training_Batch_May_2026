# Weather and Travel Advisory MCP Server

## Overview

This project is a Model Context Protocol (MCP) server that provides weather-based travel advisories using the public **wttr.in** API. It accepts a destination city, retrieves the weather forecast, normalizes the response, calculates a deterministic travel risk, and generates a structured travel advisory report.

The project was developed as part of the P004 Case Study.

---

## Features

* Validate user-provided city names
* Retrieve weather data from the wttr.in API
* Normalize raw weather data into a consistent format
* Calculate travel risk based on predefined weather conditions
* Expose MCP tools, resources, and prompts
* Generate and save a travel advisory report as JSON

---

## Project Structure

```
p004_mcp_weather_travel_advisory/

├── src/
│   ├── server.py
│   ├── tools.py
│   ├── api_client.py
│   ├── resources.py
│   ├── prompts.py
│   ├── report_writer.py
│   └── config.py
│
├── outputs/
│   └── travel_advisory_report.json
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## MCP Tools

* `validate_city_input_tool`
* `get_weather_forecast_tool`
* `normalize_weather_data_tool`
* `calculate_weather_risk_tool`
* `save_travel_advisory_tool`

---

## MCP Resources

* `resource://travel/checklist`
* `resource://travel/advisory-rules`
* `resource://weather/normalized-forecast-schema`

---

## MCP Prompts

* `travel_readiness_prompt`
* `weather_risk_summary_prompt`
* `packing_recommendation_prompt`

---

## API Used

**wttr.in**

Example:

```
https://wttr.in/Jaipur?format=j1
```

No API key is required.

---

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file if required by your project configuration.

Example:

```
WTTR_PRIMARY_URL=https://wttr.in
WTTR_FALLBACK_URL=https://wttr.is
OUTPUT_DIR=outputs
```

---

## Running the Server

```bash
python src/server.py
```

---

## Output

The generated travel advisory is saved as:

```
outputs/travel_advisory_report.json
```

---

## Notes

* Weather data is fetched from the public **wttr.in** service.
* Travel risk is calculated using fixed rule-based logic. No language model is used for risk calculation.
* MCP resources provide static reference information.
* MCP prompts are used only for generating human-readable advisory text.

---

## Limitations

* The advisory is based only on weather conditions.
* Flight, hotel, visa, medical, and disaster-related information are outside the scope of this project.
* The report should be treated as general travel guidance rather than a travel guarantee.

Due to the limited development time available for this case study, automated test cases were not completed.

To keep the implementation lightweight and focused on the required functionality, the project uses plain Python dictionaries for data structures instead of Pydantic models or a separate schema validation layer.

---

## Future Improvements

* Add comprehensive unit and integration tests.
* Introduce schema validation using Pydantic.
* Support more configurable report formats.
* Add logging and better error reporting.