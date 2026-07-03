# Project Name 
# INTELLIGENT TRAVEL BOOKING

## Business Objective and practical use
- The modern travel industry demands personalized, real-time, and highly secure customer service.
- The goal of this case study is to build an intelligent Travel Booking Assistant Agent using a tool-calling architecture. 

- Unlike a standard document-retrieval system, this agent must dynamically interact with external systems to serve the user. It will access a provided structured database to retrieve existing customer itineraries and seamlessly cross-reference that data with a live weather API to provide proactive, context-aware travel advice.

- For example, "I see you are flying to London next Tuesday; you should pack an umbrella as rain is
forecasted.".

## Technologies or frameworks used
- Pydantic AI 
This framework is used for validation purposes.

- SQLite 
This framework is used to store the data.

- Guardrails AI 
This framework is used for safety and security.

- pytest
This framework is used for evaluation and testing purposes.

- DeepEval
This framework is used for evaluation purposes.

## Functional requirements
1. There must be two tools built using Pydantic AI's decorator i.e, @agent.tool.

- Database connection tool :  Accepts user identifiers (e.g., Email or Booking ID) and retrieves   upcoming travel plans, destination cities, travel dates, and hotel details from the provided travel_data.db file.

- Weather Information tool : Accepts a location (city/coordinates) and dates, reaching out to an external Weather API to fetch current or forecasted weather conditions.

2. Dynamic Execution Logic

- The agent must interpret natural language prompts (e.g., "What is the weather going to be like for
my upcoming trip?") and deduce that it must first call the Database Tool to find out where the user
is going, and second call the Weather Tool for that specific destination.

- The agent must synthesize the outputs of both tools into a natural, helpful, and concise
conversational response.

## Non- functional requirements
1. Security, Content Moderation & Input/Output Guardrails

- Travel agents handle stressed customers; the application must be fortified against abuse using 
Guardrails AI. * Input Guardrails: Incoming user prompts must be scanned using Profanity and 
Toxicity validators. Angry or abusive prompts must be intercepted before triggering expensive LLM
or API calls, returning a standardized polite de-escalation message. * Output Guardrails: The agent's final synthesized response must be passed through the same validators to ensure brand-safe,
professional output under all circumstances.

2. Error Handling & Resilience

- The agent must gracefully handle scenarios where the booking ID does not exist in the database
or the Weather API rate-limits/times out, informing the user without exposing raw system stack
traces.

## Automated Evaluation & Testing Suites

A robust test-driven development environment using pytest paired with  DeepEval. A minimum of 10 distinct pytest functions are written.

- Two evaluation metrics are also used:
1. Answer Relevancy
2. Contextual Precision

## Folder structure of the project

└── travel-booking-agent/
 ├── db/ 
 │ └── travel_data.db
 ├── src/ 
 │ ├── agent.py 
 │ ├── tools/ 
 │ │ ├── weather.py
 │ │ └── database.py
 │ └── guardrails_config.py
 ├── tests/ 
 │ ├── conftest.py
 │ └── test_agent_metrics.py
 ├── README.md 
 └── requirements.txt 

## Development Resources & Setup Instructions

1. Database Setup (Provided): A mock SQLite database file named travel_data.db is used.It is placed in the db folder.

2. Free Weather API: To avoid managing API keys, participants are encouraged to use the Open-Meteo API (https://open-meteo.com/), which is entirely free for non-commercial use and does not
require an authentication token.

## Files and folders description 
### db/travel_data.db
- This is the database file, which contains all the information used in this project.
### Schema
- Table name : bookings

This table has multiple columns
1. id - INTEGER- primary key
2. booking_id - TEXT
3. user_name - TEXT
4. user_email - TEXT
5. destination - TEXT
6. travel_dates - TEXT
7. hotel_details - TEXT

### src folder
- This is the heart of the project.
- All the main working file of the project are in these folders only.
- Inside this, we have multiple files

1. agents.py
- This is the main file of the project and contains the agent code also.

2. guardrails_config.py
- This file contains the code for configuration of guardrails into this project.

### src/tools
- This tools folder contains 2 files i.e,

1. database.py
- decorator "@database_agent.tool" is used to initialize the tool.
- This file contains the code for the database tool.
- User inputs the query(i.e, id or email_id) and get the responses like hotel details, travel dates, destination cities etc.

2. weather.py
- decorator "@weather_agent.tool" is used to initialize the tool.
- This file contains the code for the weather tool.
- User inputs the city name and gets the weather details as output.

### tests folder
- This folder contains 2 files that contains multiple test cases i.e,

### tests/confest.py
- This file contains multiple test cases that are made by using pytest and DeepEvals together.

### tests/test_agent_metrics.py
- This file contains the test cases of the evaluation metrics i.e, answer relevancy metrics and contextual precision using DeepEval and pytest together.

### .env file
- This is the environment variable file which contains all the secrets keys and confidential information which is not to be revealed anywhere and should also be put in the .gitignore file inside .venv .

### .venv folder
- This folder is the virtual environment folder and in this folder all the requirements are being installed and whole project runs using this virtual environment only.

### README.md
- This is the main documentation file, it consists of all the relevant technical as well as non-technical information, whole description of the project and each and every file too.
- Also, it consists of the information about what commands are needed to be run, how to run the project, how to install requirements etc.

### requirements.txt
- This contains multiple required packages needed to be installed so as to run the project.

1. guardrails>=2.0.0 
2. pydantic-ai>=0.0.18
3. langchain>=0.3.25
4. langchain-community>=0.3.24
5. langchain-text-splitters>=0.3.8
6. langchain-chroma>=0.2.4
7. langchain-huggingface>=0.2.0
8. langchain-groq>=0.3.7
9. chromadb>=1.0.15
10. sentence-transformers>=4.1.0
11. python-dotenv>=1.1.0
12. pydantic>=2.11.7
13. rich>=14.0.0
14. markdown>=3.8
15. tqdm>=4.67.1
16. deepeval>=4.0.7
17. fake-database>=0.1.1

- All the versions are compatible to each other and are flexible(because of >=) and also to Python 3.12 .

- cmd command to run the project:
"pip install -r requirements.txt"


### .venv file
- This is the virual environment file.
- cmd command to create virtual environment : 
"python -m venv .venv

- To activate the virtual environment : 
".venv\Scripts\activate"

## Future improvements
- The project can be made more secure using more guardrails instead of just input and output ones.
- PydanticAI can be more broadly used.
- More tools can be made.
- Multiple agents can be made.

## How to run the project
- Run the cmd command:
"python - m src.agents"
OR
"python src/agents.py"

# Author
Vaishnavi Gupta
