#  Intelligent Travel Booking Assistant

# Project Overview
The modern travel industry demands personalized, real-time, and highly secure customer service. So here we are building a **Travel Booking Assistant Agent** which can automate our work and saves organization time for customer service support. The work of the agent is to fetch the database of customers and according to there city of travel get the current and future weather report for that city and recommend some extra measures and precaution before travelling to that city.


# Setup Instruction
1. Create virtual environmnet
```bash
uv venv
```
2. Activate environment
```bash
.venv/Scripts/activate
```
3.Install Required Libraries
```bash
uv add -r requirements.txt
```
4.Create .env file
```bash
GROQ_API_KEY=...
GROQ_MODEL=...
```
5.Guardrails set up
```bash
guardrails configure
```
6 Downloading Profanity Free Guardrails
```bash
guardrails hub install hub://guardrails/profanity_free 
```
7.Downloading Toxic Language Guardrails
```bash
guardrails hub install hub://guardrails/toxic_language
```

# Tools Used

- **database_tool**: The tool is used to get the customer data in which the details of customers like travelling date, customer name, travelling city and hotels can be fetched for more personalized information.

- **weather_tool**: Here we had used the **Open-Meteo** end point to fetch the latest weather of the city customer is travelling and so to provide him with accurate details.

# Features
- It uses 2 tools to give more accurate information to the customer.
- It automates the process of searching providing services faster.
- Here we used guardrails to validate user input.
- Before sending response to custeomer guardrails also validates LLM output.
- Pydantic Agents are used orchestrate the flow of tools.

# Project Architecture

```text
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
│   └── test_pydantic_ai_agent.py
├── README.md             
└── requirements.txt  
```

# Tech Stack
- Python
- Pydantic
- pydantic ai
- Guardrails AI

# API Endpoint Used
```bash
url = "https://api.open-meteo.com/v1/forecast"
```

# How to test the tool
```bash
python test.py
```
# How to run the project
```bash
python src/agents.py
```
# Summary
The project is describing how can we automate the our work by using pydantic tools and pydantic Agents connecting them to database and weather endpoint so that our customer service becomes faster.

# Author

**Mohd Zaid Ansari**






