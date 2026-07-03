### Project Build 5   Case Study 2: Intelligent Travel Booking Assistant

## Participant Name
Simran Kaur

## Description
The modern travel industry demands personalized, real-time, and highly secure customer service. The goal of this case study is to build an intelligent Travel Booking Assistant Agent using a tool-calling architecture using **Pydantic AI**
Unlike a standard document-retrieval system, this agent must dynamically interact with external systems to serve the user.

* Orchestration Framework:
-Pydantic AI (Leveraging typed agent states, structured responses, and strict dependency injection). 

* Database / SQL Layer: 
SQLite (Using a standard DB driver/ORM to query the provided itinerary
data). 

* Weather API: 
Any open REST API (e.g., Open-Meteo, which requires no API key, or 
OpenWeatherMap). * Security & Safety Layer: Guardrails AI (Implementing execution-stage
guardrails using Profanity and Toxicity validators).

## How to Run

```bash
pip install -r requirements.txt
python -m src.agent
```

## Libraries or packages required
```
ipykernel>=7.3.0
python-dotenv>=1.2.2
mermaid-python==0.1
pydantic-ai>=1.21.0
requests==2.32.5
pydantic_ai>=2.3.0
database-pydantic-ai==0.0.1
groq
openmeteo-requests
requests-cache
retry-requests
numpy
pandas
guardrails-ai
```
## Output explanation

Ouput is generated in natural human answer
