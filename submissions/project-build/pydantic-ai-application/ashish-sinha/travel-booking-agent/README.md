# Travel Booking Agent
Travel Booking Agent is an an intelligent Travel Booking Assistant Agent using a tool-calling
architecture. Unlike a standard document-retrieval system, this agent must dynamically interact with external systems
to serve the user. It will access a provided structured database to retrieve existing customer itineraries
and seamlessly cross-reference that data with a live weather API to provide proactive, context-aware
travel advice

---

## Tech Stack
* Python 
* Pydantic-AI
* Guardrails-AI
* DeepEval
* SQLite
* pytest
* Weather-API(Open-Meteo)


--- 

## My Project Structure
```
travel-booking-agent/
│
├── README.md
├── requirements.txt
├── .env.example
├──db/
│       └── travel_data.py
├── src/
│   ├── agent.py
│   ├── guardrails_config.py
│   ├──tools/
│       └── database.py
│       └── weather.py
│   
├── tests/
│   ├── confest.py
│   ├── test_agent_metrics.py

```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd travel-booking-agent
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
GROQ_API_KEY = your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
DB_PATH=db\travel_data.db
```
---

## Usage Guide

### Running agent

```
python src/agent.py
```

## For Run Test Suite
```
python -m pytest tests/ -v
```

## For save as text file log
```
python -m pytest tests/ -v > outputs/test_report.log
```
---
## Available Tools

1. customer_iternary_details
2. get_destination_weather_conditions
---

## Future Enhancements
* Streamlit UI
* Real-Time Weather data sync api
---

## Author
```
Ashish Sinha
```

