# Weather Travel Advisory MCP Server

A Model Context Protocol (MCP) server that provides weather-aware travel advisories using live weather data from **wttr.in**. The project demonstrates how an MCP server exposes **Tools**, **Resources**, and **Prompts** while producing a structured travel advisory report in JSON format.

The implementation follows the PRD requirements by:

- Validating user-provided destination cities.
- Fetching live weather data.
- Normalizing weather responses into a fixed schema.
- Performing deterministic weather risk analysis.
- Using MCP resources and prompts.
- Saving the final advisory as a structured JSON report.

---

# Participant 

Mohammad Anas

---
# Business Scenario

Atraveler wants to check whether the weather is suitable for travel to a city.

Example questions:

Should I travel to Jaipur this weekend?

What should I pack for Pune based on the weather?

Is Mumbai risky for outdoor travel?

Can I travel comfortably to New Delhi over the next few days?

The MCP server should not behave like a generic weather chatbot. It should 
expose well-defined MCP tools, resources, and prompts so that an MCP compatible client can use them in a structured way

---

# Business Use Case

Travel applications frequently need more than just weather forecasts. Users need actionable guidance based on expected weather conditions.

This project demonstrates how an MCP server can serve as a reusable backend for travel assistants by:

- Retrieving live weather forecasts.
- Assessing travel risk.
- Providing travel recommendations.
- Suggesting packing items.
- Producing machine-readable advisory reports.

Possible applications include:

- Travel planning assistants
- Tourism platforms
- Airline customer assistants
- Travel insurance advisory systems
- Enterprise travel management

---

# Architecture

```

User
│
▼
main.py (Workflow)
│
├── validate_city_input_tool
├── get_weather_forecast_tool
├── normalize_weather_data_tool
├── calculate_weather_risk_tool
└── save_travel_advisory_tool
│
▼
outputs/travel_advisory_report.json

```

The MCP server independently exposes:

- 5 Tools
- 3 Resources
- 3 Prompts

through FastMCP.

---

# Project Structure

```

.
├── README.md
├── requirements.txt
├── .env.example
├── main.py
│
├── outputs/
│   └── travel_advisory_report.json
│
├── sample_outputs/
│   ├── sample_jaipur_advisory.json
│   └── sample_pune_advisory.json
│
├── src/
│   ├── api_client.py
│   ├── advisory_generator.py
│   ├── prompts.py
│   ├── report_writer.py
│   ├── resources.py
│   ├── schemas.py
│   ├── server.py
│   └── tools.py
│
└── tests/
    ├── test_api_client.py
    ├── test_prompts.py
    ├── test_report_schema.py
    ├── test_resources.py
    └── test_tools.py

```

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.11+ |
| MCP Framework | FastMCP |
| Validation | Pydantic v2 |
| HTTP Client | Requests |
| Environment Variables | python-dotenv |
| Testing | pytest |
| Weather Provider | wttr.in |
| Report Format | JSON |

---

# wttr.in API Usage

Weather information is retrieved from the public **wttr.in** service.

Primary endpoint:

```

https://wttr.in/{city}?format=j1

```

Fallback endpoint:

```

https://wttr.is/{city}?format=j1

```

The API client provides:

- Connection timeout handling
- HTTP error handling
- Invalid JSON handling
- Automatic fallback support
- Structured error responses

The raw API response is never exposed in the final advisory report.

---

# MCP Tools

The server exposes five MCP tools.

## 1. validate_city_input_tool

Validates user input before making API requests.

Responsibilities:

- Empty input validation
- Minimum length validation
- City normalization

---

## 2. get_weather_forecast_tool

Retrieves live weather information from wttr.in.

Responsibilities:

- Primary endpoint request
- Fallback endpoint request
- Structured response generation

---

## 3. normalize_weather_data_tool

Converts raw weather responses into a consistent schema.

Extracts:

- Destination
- Region
- Country
- Current weather
- Three-day forecast

Calculates:

- Maximum wind speed
- Maximum rain probability
- Total precipitation

---

## 4. calculate_weather_risk_tool

Performs deterministic weather analysis.

Possible risk levels:

- LOW
- MEDIUM
- HIGH

The calculation does not use an LLM.

---

## 5. save_travel_advisory_tool

Validates the final report using Pydantic before writing:

```

outputs/travel_advisory_report.json

```

---

# MCP Resources

The server exposes three static resources.

## resource://travel/checklist

Contains a reusable travel readiness checklist.

---

## resource://travel/advisory-rules

Defines deterministic travel advisory rules used during risk assessment.

---

## resource://weather/normalized-forecast-schema

Documents the normalized weather response structure expected by the system.

---

# MCP Prompts

The server exposes three reusable prompt templates.

## travel_readiness_prompt

Generates travel readiness guidance.

---

## weather_risk_summary_prompt

Generates a weather risk explanation.

---

## packing_recommendation_prompt

Generates packing recommendations based on weather conditions.

---

# Installation

## Clone the Repository

```bash
git clone <repository-url>
cd p004_mcp_weather_travel_advisory
```

---

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file from the provided template.

```
cp .env.example .env
```

Example:

```env
OUTPUT_PATH=outputs
```

The output directory is created automatically if it does not already exist.

---

# Running the MCP Server

Start the FastMCP server:

```bash
python src/server.py
```

To verify the server registration:

```bash
fastmcp inspect src/server.py
```

Expected output:

```
Server
Tools: 5
Resources: 3
Prompts: 3
```

---

# Running the Complete Travel Advisory Workflow

The repository also contains a standalone workflow that demonstrates the complete PRD flow.

Run using a command-line argument:

```bash
python main.py Jaipur
```

or simply run:

```bash
python main.py
```

and enter the destination city when prompted.

Example:

```
Destination city: Jaipur

Generating travel advisory...

Travel advisory generated successfully.
outputs/travel_advisory_report.json
```

The workflow performs the following sequence:

```
City Validation
        │
        ▼
Weather Retrieval
        │
        ▼
Weather Normalization
        │
        ▼
Risk Calculation
        │
        ▼
Travel Advisory Generation
        │
        ▼
JSON Report Creation
```

---

# Running Unit Tests

Execute the complete test suite:

```bash
pytest
```

or

```bash
pytest tests/
```

Current coverage includes:

- City validation
- API success
- API failure
- Timeout handling
- Invalid JSON handling
- Weather normalization
- Missing weather fields
- LOW risk calculation
- MEDIUM risk calculation
- HIGH risk calculation
- MCP resources
- MCP prompts
- Report schema validation

---

# Running Integration Tests

Integration tests communicate with the live wttr.in API.

Run only integration tests:

```bash
pytest -m integration
```

Run every test except integration:

```bash
pytest -m "not integration"
```

---

# Generating Sample Reports

Generate a report for Jaipur:

```bash
python main.py Jaipur
```

Generate a report for Pune:

```bash
python main.py Pune
```

The generated report is automatically saved as:

```
outputs/
└── travel_advisory_report.json
```

Example reports are also included:

```
sample_outputs/
├── sample_jaipur_advisory.json
└── sample_pune_advisory.json
```

---

# Output Files

After a successful execution:

```
outputs/
└── travel_advisory_report.json
```

contains the latest generated travel advisory.

Sample reports are provided for reference and schema verification.

---

# Final Report Schema

Each generated report follows the structure below.

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
  "daily_forecast": [],
  "weather_risk": "LOW | MEDIUM | HIGH",
  "risk_factors": [],
  "recommended_actions": [],
  "packing_suggestions": [],
  "travel_readiness_advisory": "string",
  "weather_risk_explanation": "string",
  "resources_used": [],
  "tools_used": [],
  "prompts_used": []
}
```

The report is validated using the `TravelReport` Pydantic model before being written to disk.

---

# Validation Strategy

The project validates data at multiple stages:

- User input validation
- API response validation
- Weather normalization
- Deterministic risk calculation
- Final report schema validation

---

# Design Decisions

Several design decisions were made to keep the implementation aligned with the PRD while maintaining a clean and modular architecture.

## Deterministic Weather Risk

Weather risk is calculated using deterministic threshold rules rather than an LLM.

Reasons:

- Predictable results
- Easy to test
- Repeatable evaluations
- PRD compliant
- No dependency on AI-generated reasoning

The risk engine evaluates:

- Maximum temperature
- Rain probability
- Total precipitation
- Wind speed

and classifies the travel risk into one of three levels:

- LOW
- MEDIUM
- HIGH

---

## Separation of Responsibilities

Each module has a single responsibility.

| Module | Responsibility |
|---------|----------------|
| api_client.py | Weather API communication |
| tools.py | MCP Tool registration |
| resources.py | Static MCP Resources |
| prompts.py | MCP Prompt templates |
| advisory_generator.py | Advisory and packing recommendation generation |
| report_writer.py | JSON report generation |
| schemas.py | Pydantic validation |
| server.py | MCP server |
| main.py | End-to-end workflow execution |

This separation makes the project easier to maintain and extend.

---

## Pydantic for Validation

All major data structures are validated using Pydantic models.

Validation is performed for:

- Weather normalization
- Risk responses
- API responses
- Final travel report

This prevents invalid reports from being generated.

---

## Error Handling Strategy

The application avoids unhandled exceptions.

Common failures handled include:

- Invalid city names
- Empty input
- HTTP errors
- API timeouts
- Invalid JSON responses
- Missing weather fields
- Schema validation failures
- Output directory creation failures

Whenever possible, structured error dictionaries are returned instead of raw exceptions.

---

# Developer Notes

During development several implementation challenges were encountered.

## 1. FastMCP API Changes

The project was initially implemented assuming internal FastMCP collections such as:

```
_resources
_prompts
```

However, FastMCP 3.4 exposes public asynchronous APIs instead.

The implementation and tests were updated to use the supported public interface.

---

## 2. Import Resolution

The project needed to support both:

```
python src/server.py
```

and

```
pytest
```

Python resolves imports differently in these two execution modes.

A lightweight import fallback strategy was introduced so both commands execute successfully without changing the source code.

---

## 3. Weather Data Normalization

The wttr.in response contains deeply nested weather information.

Several values needed aggregation before becoming useful.

Examples include:

- Maximum daily wind speed
- Highest rain probability
- Total daily precipitation

These values are calculated during normalization rather than exposing the raw API response.

---

## 4. Tool Reuse Outside the MCP Server

The project objective required demonstrating the complete workflow in addition to exposing MCP tools.

Since MCP tools are registered dynamically, a lightweight registration helper was added to allow the standalone workflow (`main.py`) to reuse the exact same tool implementations without duplicating business logic.

---

## 5. Strict Schema Validation

During integration testing, report generation initially failed because the normalized weather response included additional metadata not defined in the final report schema.

This was resolved by ensuring only schema-compliant fields are passed into the final `TravelReport`.

---

# Known Limitations

Current limitations include:

- Weather data depends on the availability of wttr.in.
- Only a three-day forecast is processed.
- Risk calculation is based on predefined thresholds.
- Advisory text is deterministic rather than AI-generated.
- Offline execution is not supported.
- Historical weather analysis is not included.

These limitations are acceptable for the current project scope and align with the PRD requirements.

---

# Future Improvements

Potential future enhancements include:

- Support for additional weather providers.
- Configurable weather risk thresholds.
- Multi-language advisory generation.
- Extended seven-day forecasts.
- PDF travel advisory export.
- Email or notification delivery.
- Travel recommendations based on seasonal weather.
- Integration with flight and hotel planning services.
- Interactive web dashboard.
- Persistent advisory history.

These improvements are intentionally outside the current project scope.

---

# Assumptions

The implementation assumes:

- wttr.in is reachable during execution.
- City names are valid geographical locations.
- The weather API returns the expected JSON format.
- The generated report represents the latest weather forecast available.

---

# Conclusion

This project demonstrates how the Model Context Protocol (MCP) can be used to expose reusable Tools, Resources, and Prompts while producing a structured travel advisory workflow.

The implementation follows the PRD by:

- exposing five MCP tools,
- exposing three MCP resources,
- exposing three MCP prompts,
- retrieving live weather data,
- normalizing weather responses,
- calculating deterministic travel risk,
- generating travel recommendations,
- validating the final report with Pydantic,
- and saving the advisory as a structured JSON document.

