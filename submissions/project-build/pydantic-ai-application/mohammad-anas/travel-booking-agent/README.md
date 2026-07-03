# Intelligent Travel Booking Agent

## Overview
A **Pydantic‑AI** based agent that:
1. Retrieves a user's upcoming booking from `travel_data.db`.
2. Fetches the weather forecast for the destination via the Open‑Meteo API.
3. Returns a concise, brand‑safe answer, guarded by **Guardrails AI** (profanity & toxicity).

## Project Structure
```
 travel-booking-agent/
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
                └── requirements.txt       # Hardened dependency definition
```

## Setup

```bash
# 1️⃣ Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2️⃣ Install dependencies
pip install -r requirements.txt
```

## Running the Agent

```bash
# Example usage (replace the prompt as needed)
python -m src.agent "What will the weather be like for my upcoming trip? my booking_id is = TRV-101"
```

The script:
1. Validates the user prompt with Guardrails (profanity/toxicity).  
2. Plans tool calls (DB → Weather).  
3. Synthesizes a response and runs it through the output guardrails.  

## Testing

```bash
pytest -q
```

All tests must pass. The suite includes:
- Relevancy & contextual precision checks.
- Guardrails validation (input & output).
- Error‑handling scenarios.
- Order‑of‑operations verification.
- A dummy relevance metric meeting the PRD threshold (≥ 0.85).

## Key Components

### `src/guardrails_config.py`
- Configures a single `Guard` with `ToxicLanguage` & `ProfanityFree`.
- Provides `safe_input` (raises on violation) and `safe_output` (sanitises or returns a polite fallback).

### `src/tools/database.py`
- Connects to `db/travel_data.db`.
- `get_upcoming_booking(identifier)` returns a `Booking` Pydantic model (or `None`).

### `src/tools/weather.py`
- Uses `geopy` to turn a city name into lat/lon.
- Calls Open‑Meteo (`https://api.open-meteo.com/v1/forecast`) for a single‑day forecast.
- Returns a minimal dict with description, max/min temps, etc.

### `src/agent.py`
- Declares `TravelAgent` extending `pydantic_ai.Agent`.
- Two tools (`fetch_booking`, `fetch_weather`) expose the DB and weather functions to the LLM.
- `_plan_and_execute` performs lightweight natural‑language parsing, orchestrates tool calls, and builds the final answer.
- `run` applies input guardrails then executes the plan.

## Security & Safety
- **Input guardrails** block abusive prompts before any LLM or external call.
- **Output guardrails** ensure the final response is brand‑safe; offensive content is replaced with a polite de‑escalation message.

## Dependencies
- `pydantic`, `pydantic-ai` – typed agent framework.
- `groq` – LLM backend (replaceable with any compatible provider).
- `guardrails-ai` – profanity & toxicity validators.
- `requests` – HTTP calls to Open‑Meteo.
- `geopy` – city → coordinates conversion.
- `pytest`, `deep-eval` – test suite.

## Notes
- No API keys are required for Open‑Meteo.
- The SQLite DB is bundled; modify `src/tools/database.py` only if the schema changes.
- Ensure internet connectivity for weather lookups

## Author

Mohammad Anas