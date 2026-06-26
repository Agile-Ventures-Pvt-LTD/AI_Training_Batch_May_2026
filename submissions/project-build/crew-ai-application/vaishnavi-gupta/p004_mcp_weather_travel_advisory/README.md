# Weather Travel Advisory Project
- This project is all about providing weather information of different locations along with advice of travelling at that partiular location.
- As per the weather conditions of a particular place, this system gives advice about what should be carried to travel at that place, or what should be worn as per temperature, wind, rainfall etc. as well as precuations and readiness to maintain at that place.

## Business Use Case
- Along with the weather conditions, travel advices are given too.
- Small details related to travelling and weather is provided.

## Project Structure
p004_mcp_weather_travel_advisory/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── src/
│ ├── server.py
│ ├── tools.py
│ ├── resources.py
│ ├── prompts.py
│ ├── api_client.py
│ ├── schemas.py
│ └── report_writer.py
│
├── tests/
│ ├── test_api_client.py
│ ├── test_tools.py
│ ├── test_resources.py
│ ├── test_prompts.py
│ └── test_report_schema.py
│
├── outputs/
│ └── travel_advisory_report.json
│
└── sample_outputs/
 ├── sample_jaipur_advisory.json
 └── sample_pune_advisory.json

## Files/folders description

### .env.example
- This file contains the secret variable i.e,
1. WTTR_PRIMARY_URL
2. WTTR_FALLBACK_URL
3. OUTPUT_PATH

### requirements.txt
- This file contains the required packages and frameworks i.e, 
- fastmcp==2.12.2
  mcp-use==1.7.0
  python-dotenv==1.1.1
  requests==2.32.5
  pydantic>=2.10,<3.0 
  pytest

### README.md
- This file is a documentation file.
- This file stores each and every information of the project i.e,
1. Folder structure.
2. How to run the project.
3. Various commands used in the project.
and many more...

### .venv folder
- This is the virtual environment in which the whole project is running.
- command to create .venv - python -m venv .venv
- command to activate .venv - .venv\Scripts\activate

### outputs folder
- This folder contains file that store output i.e,
1. travel_advisory_reports.json (It consists of output generated for travel advisory.)

### sample outputs folder
- This folder consists of 2 files:
1. sample_jaipur_advisory.json (This file contains the data about the travel advisory a traveller should have before moving to Jaipur city.)

2. sample_pune_advisory.json (This file conatains the data about the travel advisory a traveller should have before moving to Pune city.)

### src folder
- This folder is one of the most important folder as it contains file which have codes of main working of the project.

### api_client.py
- This file contains mostly the variable configuration part.

### prompts.py
- As mentioned in the PRD, this file contains 3 prompts have to be designed i.e,
1. travel_readiness_prompt
2. weather_risk_summary
3. packing_recommendation

### report_writer.py
- This file contains the code to write the report as an output.

### resources.py
- Resources are one of the components of MCP.
- In this file, there are 3 resources i.e,
1. resource://travel/checklist
2. resource://travel/advisory-rules
3. resource://travel/normalized-forecast-schema

### schemas.py
- Schema == Design
- This file contains the code for the output format of the project.

### tools.py
- Tools are also one of the 3 components of MCP.
- This file contains 5 tools i.e,
1. validate_city_input_tool
2. get_weather_forecast_tool
3. normalize_weather_data_tool
4. calculate_weather_risk_tool
5. save_travel_advisory_tool

### tests folder
- This folder conatains all the files which perform testing i.e,

### test_api_client.py
- This file tests that the client is working correctly or not.

### test_report_schema.py
- This file tests the output schema in which report will be generated.

### test_resources.py
- This file tests the resources components of the project.

### test_tools.py
- This file tests the tools components of the project.

### test_prompts.py
- This file tests the prompts components of the project.

## How to run the project
- Run the command in the terminal - python api_client.py
## Author 
- Vaishnavi Gupta