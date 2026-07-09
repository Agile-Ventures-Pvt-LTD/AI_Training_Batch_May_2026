# : Weather and Travel Advisory MCP Server Using wttr.in API

## Overview
A traveler wants to check whether the weather is suitable for travel to a city.
Example questions:
Should I travel to Jaipur this weekend?
What should I pack for Pune based on the weather?
Is Mumbai risky for outdoor travel?
Can I travel comfortably to New Delhi over the next few days
# Project Structure
```text
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
```
---
# Environment Variables
Create `.env`
---
 Activate Environment
   ```bash
    source .venv/Scripts/activate
    uv pip install -r requirements.txt
```
---
# run this
```bash
python src/report_writer.py  # for travel_advisory_report.json
python src/api_client.py # for the client object
python src/server.py
```
---
