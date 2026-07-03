#  Intelligent Travel Booking Assistant

We have to create the travel agent which helps the user about the trip. It will fetch the database and then according to the travel date , it checks for the temperature and weather condition. Then it will suggest the tips according to the weather at the real time.

#  Business Objective & Background

The modern travel industry demands personalized, real-time, and highly secure customer service. The
goal of this case study is to build an intelligent Travel Booking Assistant Agent using a tool-calling architecture. 

Unlike a standard document-retrieval system, this agent must dynamically interact with external systems to serve the user. It will access a provided structured database to retrieve existing customer itineraries and seamlessly cross-reference that data with a live weather API to provide proactive, context-aware travel advice (e.g., "I see you are flying to London next Tuesday; you should pack an umbrella as rain is forecasted.")

# Tech Stack

- Orchestration Framework: Pydantic AI
- Database / SQL Layer: SQLite
- Weather API: Any open REST API e.g., Open-Meteo
- Security & Safety Layer: Guardrails AI ( Profanity and Toxicity validators)
- Evaluation Framework: pytest, DeepEval

# Directory Standard

```bash
submissions/
└── project-build/
    └── pydantic-ai-application/
        └── vikash-kumar/
            └── travel-booking-agent/
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

```


# Environment Variables

```bash
GROQ_API_KEY=

GROQ_MODEL=llama-3.3-70b-versatile

HF_TOKEN=
```

# Setup

```python
uv venv

.venv\Scripts\activate

uv pip install -r requirements.txt
```

# Running the files

```python
python src/agent.py
```

# Testing

```python
pytest tests/test_agent_metrics.py
```

# Future Improvement

We can use some more precise weather api tool which can give much better and precise result.

# Author

Vikash Kumar