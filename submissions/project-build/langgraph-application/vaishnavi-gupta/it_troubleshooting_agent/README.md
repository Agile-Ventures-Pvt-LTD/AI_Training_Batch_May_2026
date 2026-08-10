# Project - Title
IT Troubleshooting Agent with Tool-using Workflow using LangGraph


## Product Goal ( Business Objective)
Build an IT Troubleshooting Agent that can:
- Understand the user’s IT issue.
- Classify the issue type.
- Retrieve relevant troubleshooting guidance using RAG. Use tools to inspect users, devices, known  incidents, tickets, and diagnostics.
- Execute a sequential diagnostic workflow.
- Run selected diagnostic checks in parallel where useful.
- Branch conditionally based on issue type, severity, missing data, and tool 
  results.
- Generate a safe troubleshooting plan.


## Primary users
- IT Support Engineer
- Helpdesk Agent


## Dataset provided
it_troubleshooting_agent_dataset.zip


## Method of Implementation
Choice 1: LangGraph Prebuilt ReAct Agent
Choice 2: Custom LangGraph Agent


## LangGraph Workflow Patterns
### Sequential pattern
- Every action is completed one after the other in a particular sequence.

### Parallelization pattern
- All the tasks are executed parallely or simultaneously.

### Conditional Pattern
- Nodes/functions are executed based on some conditions.
- Routers usually decide to which node will the state move as per conditions.


## Choice of Implementation
- Choice 1: LangGraph Prebuilt ReAct Agent

## Project Structure
it_troubleshooting_agent/
│
├── app.py
├── config.py
├── loaders.py
├── retrievers.py
├── db_utils.py
├── tools.py
├── graph.py
├── prebuilt_agent.py
├── prompts.py
├── output_parser.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ ├── knowledge_base/
│ └── database/
│
├── vector_store/
│
└── outputs/
 ├── sample_run_outputs.md
 └── evaluation_results.json

### app.py
- Main file of the whole project.
- The project runs from app.py.

### config.py
- Contains the configuration of api_key and model.

### loaders.py
- Load the database from the folder using PyPDFLoader.

### retrievers.py
- Retrieve the chunks that are stored in the vector database.

### db_utils.py
- Provides reusable database utility functions for connecting to SQLite like, executing queries, retrieving records, and fetching database schema information.

### tools.py
- Contains the definition of all the tools that are used in the execution of the LangGraph.

### prebuilt_agent.py
- Consists of the main code and working of the LangGraph agent.

### prompts.py
- Consists of  the system prompt that will be given to the system to control its behaviour.

### output_parser.py
- Consists of the code that saves the retrieved output in the evaluation_results.json file.

### database
- Contains all the data on which the whole working is done.
- Database: it_support.db

### vector_score
- The database that stores vector embeddings of the chunks created.

### outputs
- In this folder:
- evaluation_results.json - Actual outputs are created.
- sample_run_outputs.md - Outputs of sample queries are stored there.

## Virtual environment setup
Command:
cmd: python -m venv .venv

## .env
- GROQ_API_KEY=
- GROQ_MODEL=llama-3.3-70b-versatile
- DB_PATH=data/database/it_support.db
- KB_PATH=data/knowledge_base
- VECTOR_STORE_PATH=vector_store
- EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
- CHUNK_SIZE=900
- CHUNK_OVERLAP=120
- TOP_K=4


# Requirements
- langgraph==0.6.6
- langchain==0.3.27
- langchain-core==0.3.74
- langchain-community==0.3.19
- langchain-groq==0.3.7
- langchain-chroma==0.2.2
- chromadb>=0.6.3
- sentence-transformers===5.1.2
- python-dotenv==1.1.1
- pydantic==2.11.7


## Installing requirements
Command:
cmd: pip install -r requirements.txt


## How to run the project
Command
cmd: python app.py

## Difference between Choice 1 and Choice 2
           Choice 1                                            Choice 2
Prebuilt agent is simpler to implement.             More complex as compared to Choice 2.
Do not contain nodes,edges and graph structure.     Contains nodes, edges and whole graph structure.
Less user interference.                             More human interference. 


# Author
Vaishnavi Gupta
