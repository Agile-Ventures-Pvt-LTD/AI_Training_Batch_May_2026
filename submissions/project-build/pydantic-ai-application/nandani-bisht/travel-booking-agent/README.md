## Intelligent travel Booking Assistant

```System Identifier:``` travel-booking-agent

## Participant Name
Nandani Bisht


## Business Objective & Background 

The modern travel industry demands personalized, real-time, and highly secure customer service. The
goal of this case study is to build an intelligent Travel Booking Assistant Agent using a tool-calling
architecture. see the structure of the code 
Unlike a standard document-retrieval system, this agent must dynamically interact with external systems
to serve the user. It will access a provided structured database to retrieve existing customer itineraries
and seamlessly cross-reference that data with a live weather API to provide proactive, context-aware
travel advice (e.g., "I see you are flying to London next Tuesday; you should pack an umbrella as rain is
forecasted.").


## Project Structure
submissions/
└── project-build/
 └── pydantic-ai-application/
 └── firstname-lastname/
 └── travel-booking-agent/
 ├── db/ # Must contain the provided database
 │ └── travel_data.db
 ├── src/ # Core application source code
 │ ├── agent.py # Pydantic AI agent definition
 │ ├── tools/ # Tool implementations
 │ │ ├── weather.py
 │ │ └── database.py
 │ └── guardrails_config.py
 ├── tests/ # pytest & DeepEval suites
 │ ├── conftest.py
   └── test_agent_metrics.py
 ├── README.md # Setup, architecture, and run instructions
 └── requirements.txt 

## Env. variables
``` 
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```


## Install dependencies
```
pip install -r requirements.txt
```

## Run the travel Assistant 
```
python travel_assistant.py
```

