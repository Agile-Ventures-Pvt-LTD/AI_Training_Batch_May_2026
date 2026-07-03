# Intelligent Travel Booking Assistant

The modern travel industry demands personalized, real-time, and highly secure customer service. The goal of this case study is to build an intelligent **Travel Booking Assistant Agent** using a tool-callingarchitecture. 

---
## Objective
Unlike a standard document-retrieval system, this agent must dynamically interact with external systems to serve the user. It will access a provided structured database to retrieve existing customer itineraries and seamlessly cross-reference that data with a live weather API to provide proactive, context-aware travel advice (e.g., "I see you are flying to London next Tuesday; you should pack an umbrella as rain is forecasted.").

---
## Project Structure
```

travel-booking-agent/
├── db/                    
│   └── travel_data.db
├── src/                   
│   ├── agent.py           
│   ├── tools/             
│   │   ├── weather.py
│   │   └── database.py
│   └── guardrails_config.py
├── tests/                 
│   ├── conftest.py
│   └── test_agent_metrics.py
├── README.md              
└── requirements.txt       
```
---
## Tech Stack
- Python
- Groq LLM
- deepeval
- pydantic-ai
- guardrails-ai

---

##  Environment Variables & Setup

1. Clone the project repository code into your local development space.
    ```bash
    git clone <repository-url>
    ```
2. Initialize and activate an isolated virtual workspace environment:
   ```bash
   python -o -m venv .venv
   On Windows use: .venv\Scripts\activate
   ```
3. Install the application dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure a `.env` instance referencing the keys inside `.env.example`:
   ```env
   GROQ_API_KEY=your_groq_api_credential_key_here
   GROQ_MODEL=groq:llama-3.3-70b-versatile
   DB_PATH=db/travel_data.db
   ```
---
## Running the Pydantic Agent
### Guardrails-Hub Setup

Before running agent you must setup Guardrails Configuration

Open Terminal & run this command:
```bash
guardrails configure
```
Then hit Y button two times and paste your **Guardrails-AI API Token**.

After this process you need to install validators through these commands.
```bash
guardrails hub install hub://guardrails/profanity_free
guardrails hub install hub://guardrails/toxic_language
```
Guardrails Configuration is Complete Now run the agent.

```bash
python src/agent.py
```
---

## Application Workflow

```
User Query
      │
      ▼
    Agent
      │
      ▼
  Guardrails
      │
      ▼
     LLM
      │
      ▼
   tool call
      │
      ▼
Tool Response
      │
      ▼
    Agent
      │
      ▼
Final Response
```
---

## Running Tests

Execute all test cases using:

```bash
pytest test_agent_metrics.py
```

---

## Future Improvements

Possible enhancements include:

- Multi-step tool execution
- Automatic transition lookup by status name
- Conversation memory
- Tool result caching
- Rich terminal interface

---
## Author

**Pranay Gupta**