#  Weather and Travel Advisory 

# Participant Name

**Mohd Zaid Ansari**

# Project Overview
The project is about using MCP Server efficiently to fetch weather data from wttr.in. In this project we are using MCP Server
to make server and client to get the weather of the current location and help anyone travelling to get a good travel advisory.
In this project we had used 5 tools to get weather, calculate risk, give travel advisory to end user so they can plan there travel efficiently. We also implmented resources and prompts to read the advisory and give more accurate travel advisory to our user.

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

4.Create .env file
```bash
WTTR_PRIMARY_URL=...
WTTR_FALLBACK_URL=...
OUTPUT_PATH=outputs
```
# Features
 - Uses tools for different tasks.
 - Server file is used to test the performance.
 - Each tools perform different task so to get good advisory.
 - Reduce manual lookup everytime to weather and manually checking advisory.
 - Helps to plan travel more efficently

 # Project Architecture

 ```text
ProjectBuild8/
│
├── .env.example                  
├── requirements.txt      
├── run_manual_scenarios.py 
│
├── src/
│   ├── __init__.py      
│   ├── server.py         
│   ├── tools.py          
│   ├── api_client.py     
│   ├── resources.py      
│   └── prompts.py        
│
├── tests/              
│   ├
│   ├── test_tools.py
│   ├── test_resources.py
│   ├── test_prompts.py
│  
│
├── outputs/              
│   └── travel_advisory_report.json
│
```

# Tech Stack

- Python
- MCP
- FASTMCP
- mcp tools
- mcp prompts
- mcp resources

# Available Tools

Tools:
- validity_city_input_tool
- get_weather_forecast_tool
- normalize_weather_data_tool
- calculate_weather_risk_tool
- save_travel_advisory

# Available Resources

Resources:
- travel_checklist
- travel_rule
- forecast_schema

# Available Prompts

Prompts:
- travel_readiness_prompts
- weather_risk_summary_prompts
- packing_recommendation_prompts

# Future Improvements

- Add more tools do get more information.
- We can use Agent to get response
- We can use Anti-Gravity, VS code client to run our server.


# Author

**Mohd Zaid Ansari**
