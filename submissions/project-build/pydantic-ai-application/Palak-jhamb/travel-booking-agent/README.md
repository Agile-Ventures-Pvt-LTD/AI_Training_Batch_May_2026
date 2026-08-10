# Project
## Project Build 5 (P005) – Case Study 2: 
## Project Name: Intelligent Travel Booking Assistant 
### Submitted By: Palak
### Objective:
The modern travel industry demands personalized, real-time, and highly secure customer service. The
goal of this case study is to build an intelligent Travel Booking Assistant Agent using a tool-calling
architecture. 
Unlike a standard document-retrieval system, this agent must dynamically interact with external systems
to serve the user. It will access a provided structured database to retrieve existing customer itineraries
and seamlessly cross-reference that data with a live weather API to provide proactive, context-aware
travel advice.

### How to do set up
1. initialize uv
```
uv init
```
2. create enviroment
```
uv venv 
```
3. add all requirements
```
uv add -r requirements.txt
```
4. add all api and configrations in **.env** file

5. configure guardrail
```
guardrails configure
```
6. Add profinity free using guardrail hub
```
guardrails hub install hub://guardrails/profanity_free
```
7. Add toxicity using guardrail hub
```
guardrails hub install hub://guardrails/toxic_language
```



**set-up is complete**

### Requirements.txt
```
groq>=1.2.0
ipykernel>=7.2.0
python-dotenv>=1.2.2
deepeval==4.0.7
guardrails-ai>=0.6.7
presidio-analyzer>=2.2.363
presidio-anonymizer>=2.2.363
database-pydantic-ai
```



### How to run project
```
uv run main.py
```

### Architecture
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

### How to run test
```
uv run -m pytest tests/conftest.py -v
```