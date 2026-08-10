# Project-04 Case-2
## Project Title
###  Weather and Travel Advisory MCP Server Using wttr.in API
### Submitted By: Palak
### 1. Project overview:

### 2. Requirements
fastmcp>=3.1.0
ipython>=9.10.0
requests>=2.32.5
python-dotenv>=1.2.2
mcp-use>=1.6.0
langchain-groq>=1.1.2
pypdf>=6.7.5
pydantic-ai>=1.78.0

### 3.Setup instructions

Steps for set-up are as follows:
1. initialize uv
```bash
uv init
```

2. create Environment 
```bash
uv venv
```
3. install requirements
```bash
uv add -r requirements.txt
```

**set-up part is completed!!!**

---


### 4.Environment variable setup

To set any Environment variable, do the following:
1. first create Environment file named **.env**
2. add your api key here 
```python
API_KEY=zwxx2.....
```
3. Load the api in any folder or file with the help of os
```bash
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['API_KEY'] = os.getenv("API_KEY")
```

---

### 5. Folder structure

p004_mcp_weather_travel_advisory/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── src/
│   ├── server.py
│   ├── tools.py
│   ├── resources.py
│   ├── prompts.py
│   ├── api_client.py
│   ├── schemas.py
│   └── report_writer.py
│
├── tests/
│   ├── test_api_client.py
│   ├── test_tools.py
│   ├── test_resources.py
│   ├── test_prompts.py
│   └── test_report_schema.py


### 6. How to run mcp
To run the client type command in terminal
```python
uv run src/api_client.py
```

This will run mcp client in terminal


### 7.Components of MCP
There are major 2 components of MCP
1. **server**
2. **client**

#### **Server:**
It is the main component that has all tools, resources and prompts.
- Tools: validate_city_input_tool,get_weather_forecast_tool,normalize_weather_data_tool,calculate_weather_risk_tool,save_travel_advisory_tool
- Resources: get_checklist,get_advisory,get_schema
- prompts: travel_readiness_prompt,weather_risk_summary_prompt,packing_recommendation_prompt

#### **Client:**

This is the interacting interface with llm that is use to respond to user query.




