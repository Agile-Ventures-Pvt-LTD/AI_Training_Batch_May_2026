# Project Build 5 (P005) – Case Study 2: Intelligent Travel Booking Assistant

## Business Objective & Background

The modern travel industry demands personalized, real-time, and highly secure customer service. The
goal of this case study is to build an intelligent Travel Booking Assistant Agent using a tool-calling
architecture

## Tech Stack 
```bash
groq 
pydantic-ai >= 2.4.0
python-dotenv >= 1.2.2
pytest >= 9.1.1
pydantic>=2.0.0
httpx>=0.25.0
pytest-asyncio>=0.23.0
deepeval>=1.0.0
openmeteo-requests >= 1.7.5
requests-cache
retry-requests 
guardrails-ai >= 0.10.2
pydantic-ai[groq]
```
## Setup 
crate venv
```bash
uv venv
```
create requirements.txt
```text
groq 
pydantic-ai >= 2.4.0
python-dotenv >= 1.2.2
pytest >= 9.1.1
pydantic>=2.0.0
httpx>=0.25.0
pytest-asyncio>=0.23.0
deepeval>=1.0.0
openmeteo-requests >= 1.7.5
requests-cache
retry-requests 
guardrails-ai >= 0.10.2
```
install the requirements by activating the venv
```bash
.venv\Scripts\activate
```
then
```bash
uv pip install -r rquirements.txtx
```
---
## set the .env
GROQ_API_KEY=your_api_key

## NOTE
you must download the guardrail using the below command in terminal
```bash
guardrails configure
```
- You will need API key - create it by clicking the link

- provide api key
then install the guardrails in terminal using the following command

```bash
guardrails hub install hub://guardrails/toxic_languag
guardrails hub install hub://guardrails/profanoty_free
```
## folder Structure
---
                /travel-booking-agent/
                ├── db/                    # Must contain the provided database
                │   └── travel_data.db
                ├── src/                   # Core application source code
                │   ├── agent.py           # Pydantic AI agent definition
                │   ├── tools/             # Tool implementations
                │   │   ├── weather.py
                │   │   └── database.py
                │   └── guardrails_config.py
                ├── tests/                 # pytest & DeepEval suites
                │   ├── conftest.py
                │   └── test_agent_metrics.py
                ├── README.md              # Setup, architecture, and run instructions
                └── requirements.txt       # Hardened dependency definitions
---

# Tools:
get_user_bookings
- for getting the booking details from database

get_weather_forecast
- for getting weather updates
NOTE: Helper function is to be created for converting the city names to Longitude and altitude

# Final Output 
Issue with circular import - hence did't run as expected 
