# MCP Weather and Travel Advisory
This MCP based system provides an automated data processing pipeline that connects to weather streaming data by use of wttr.in api key and converts raw data into a standardized schema, it evaluates environmental risk thresholds, and saves a structured travel safety report to disk for users.

---

## System Features

The server processes destinations through five sequential processing stages:
1. Input Validation: Clean the  raw input text and creates normalized parameters for API queries.
2. Weather Fetching: Collects localized conditions from weather endpoints with automatic failover support.
3. Data Normalization: Converts raw API metadata into a clean internal data structure.
4. Risk Assessment: Tests normalized metrics against safety logic parameters (Extreme Heat >= 40°C, Heavy Rain >= 20mm, High Wind >= 40 km/h) to assign it as LOW, MEDIUM, or HIGH risk rating.
5. Report Persistence: Writes the compiled final report file directly to local storage.

--- 

## My Project Structure
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

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd p004_mcp_weather_travel_adivosry
```

### 2. Create Virtual Environment

```bash
uv venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```
WTTR_PRIMARY_URL=https://wttr.in
WTTR_FALLBACK_URL=https://wttr.is
OUTPUT_PATH=outputs
```
---

## Usage Guide

### Running Local Server Tests
You can run a quick local test of the server directly from your terminal using the built-in --sample-city utility flag.
```
python src/server.py --sample-city "Jaipur"
```
The system will display the execution progress of all stages in the terminal and write the result file to ```outputs/travel_advisory_report.json.```

### Launching the MCP Server
To boot up the server as an active background network process run:
```
python src/server.py
```

## For Run Test Suite
```
python -m pytest tests/ -v
```

## For save as text file log
```
python -m pytest tests/ -v > outputs/test_report.log
```

## Author
```
Ashish Sinha
```

