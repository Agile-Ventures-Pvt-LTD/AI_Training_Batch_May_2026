# Project build case 06 - Travel booking agent

This project demonstrates the use of Pydantic AI, Guardrails, sqlite and open mateo api. The agent uses tool calling to provide travel qadvice with weather conditions, also uses guardrails to prevent profanity and toxic language.

---

## Business use case

The modern travel industry demands personalized, real-time, and highly secure customer service. The
goal of this case study is to build an intelligent Travel Booking Assistant Agent using a tool-calling
architecture.
Unlike a standard document-retrieval system, this agent must dynamically interact with external systems
to serve the user. It will access a provided structured database to retrieve existing customer itineraries
and seamlessly cross-reference that data with a live weather API to provide proactive, context-aware
travel advice (e.g., "I see you are flying to London next Tuesday; you should pack an umbrella as rain is
forecasted.").

---

## Tech stack

- Python 3.13
- Pydantic AI
- SQLite
- Guardrails
- Deepeval

## Directory Structure

```bash
submissions/
└── project-build/
 └── pydantic-ai-application/
 └── firstname-lastname/
 └── travel-booking-agent/
 ├── db/ # contain the provided database
 │ └── travel_data.db
 ├── src/ # Core application source code
 │ ├── agent.py # Pydantic AI agent definition
 │ ├── tools/ # Tool implementations
 │ │ ├── weather.py
 │ │ └── database.py
 │ └── guardrails_config.py
 ├── tests/ # pytest & DeepEval suites
 │ ├── conftest.py
 │ └── test_agent_metrics.py
 ├── README.md # Setup, architecture, and run instructions
 └── requirements.txt # Hardened dependency definitions
```
---

## Setup & Run Instructions

### Prerequisites
- Python 3.13+
- Groq API Key 

### 1. Installation

Create a virtual environment and install all dependencies:
```bash
uv venv
uv add install -r requirements.txt

```

### 2. Must Install Guardrails Validators
Download the toxicity and profanity free validators from the Guardrails hub:
```bash
guardrails hub install hub://guardrails/toxic_language
guardrails hub install hub://guardrails/profanity_free
```

### 3. Running the Agent 
```bash
python src/agent.py
```

---

## Evaluation & Testing

The evaluation is managed via **pytest** and **DeepEval** as per case study requirements. The suite verifies:
- **Answer Relevancy** 
- **Contextual Precision** 

To run tests:
```bash
uv run pytest
```

## Sample query

**Execution of a Sample query -This showcases the execution of db tool**
```bash
(travel-booking-agent) PS C:\Users\Taniya Gupta\Desktop\Project\travel-booking-agent> python src/agent.py
Project build 05_case study 02
**Query: i am going to japan today**
C:\Users\Taniya Gupta\Desktop\Project\travel-booking-agent\.venv\Lib\site-packages\guardrails\validator_service\__init__.py:73: UserWarning: Could not obtain an event loop. Falling back to synchronous validation.
  warnings.warn(
Response: Here’s the booking we have for a trip to Japan:

| Booking ID | Name      | Email                | Destination      | Travel Dates               | Hotel Details               |
|------------|-----------|----------------------|------------------|---------------------------|----------------------------|
| TRV-102    | Bob Jones | bob.j@example.com    | Tokyo, Japan     | 2026‑09‑01 to 2026‑09‑10   | Shinjuku Granbell Hotel    |

If this is you, enjoy your trip to Tokyo! Let me know if you need anything else—such as travel tips, itinerary changes, or additional reservations. Safe travels!
```

---

**Execution of sample query-This showcases the implementation of project**
- The destination, current weather and travel dates of user "Diana Prince" is fetched

```bash
Query: Hi i am Diana Prince
Response: **Current Weather in Miami, USA**

- **Temperature:** 29.3 °C (≈ 84.7 °F)  
- **Condition:** Clear skies  

**What this means for your trip (Nov 5 – Nov 8, 2026):**

1. **Pack Light & Breathable Clothing** – Expect warm, sunny weather. Bring shorts, T‑shirts, sundresses, and a light sweater for cooler evenings (especially near the water).  
2. **Sun Protection** – A high SPF sunscreen, sunglasses, and a hat are essential; the UV index is typically high under clear skies.  
3. **Stay Hydrated** – Even though it’s not extremely hot, the humidity in Miami can make it feel warmer. Carry a reusable water bottle.  
4. **Outdoor Activities** – Great conditions for beach time at Fontainebleau Miami Beach, pool lounging, or exploring South Beach.  
5. **Evening Plans** – Nights are comfortable but can dip slightly; a light jacket or cardigan will keep you comfortable for dinner or nightlife.  
6. **Rain Possibility** – While the forecast shows clear skies now, Miami’s weather can change quickly. Keep a compact umbrella or a light rain jacket handy just in case.  

**Quick Checklist**

- ☑️ Light, breathable outfits  
- ☑️ Sun hat, sunglasses, SPF 30+ sunscreen  
- ☑️ Reusable water bottle  
- ☑️ Light sweater or jacket for evenings  
- ☑️ Optional compact umbrella  

Enjoy your stay at Fontainebleau Miami Beach! Let me know if you need recommendations for restaurants, activities, or anything else.
Query: 
```

---

