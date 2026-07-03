# `P005 - Travel Booking Agent`

This is a Travel Booking Agent built with **Pydantic, GroqLLM, Open Meteo**, and **Sqlite**.

Here, Agent can use a language model to interact with travel data db and weather api to answer user queries.

---

# Project Structure

```
travel-booking-agent
├── .cache.sqlite
├── .env
├── README.md
├── data
│   └── travel_data.db
├── requirements.txt
└── src
    ├── __init__.py
    ├── agent.py
    └── utils
        ├── config.py
        ├── db_conn.py
        ├── geolocation.py
        └── prompts.py
```

---

# Environment Variables (Configuration)

Create a `.env` file in the project root and add the corresponding values.

```env
GROQ_API_KEY=...

OUTPUT_PATH=outputs
SRC_PATH=src
UTILS_PATH=utils
DATA_PATH=data
```

---


# Available MCP Tools

The Agent exposes the following tools.

| Tool | Description |
|------|-------------|
| get_user_details | Fetches user details from the database using email or booking id. |
| get_weather_details | Fetches weather data for a location during a period of days. |


---

# Running the Server (stdio)

Start the Agent Loop:

```bash
python src/agent.py
```
The agent returns output in natural language.


---

# Notes

The project is missing the following requirements:
- Guardrails config
- DeepEval Tests

What the project displays:
- Clean and refined tool usage.
- Agent loop in asnychronous mode.

---

# `THANK YOU`