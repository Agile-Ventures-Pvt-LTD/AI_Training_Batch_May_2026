# CAPSTONE -1 CASE STUDY 1
## Supply Chain Crisis Management and Logistics ReRouter
## Submitted by: Palak

### Project Overview
A major shipping port has suddenly become unavailable because of a strike, weather disruption, or
operational failure.
A shipment is already in transit and must be rerouted.
so logistics team has to manage this flow and want to get details regarding available routes, available paths and other details to help customer get thier orders on time.


### Solution Approach
To overcome this situation, an architecture is made to help the team get required results
- an langgraph agent that is used to get information based on incident id
- it also has an rag based tool that is used to retrive data from knowledge base


### Architecture
```
Incident
↓
LangChain Extraction
↓
RAG Rule Retrieval
↓
Route and Warehouse Tools
↓
LangGraph Decision and Retry Loop
↓
Final Report
```

### Project structure
```
├── data/
│   ├── logistics_knowledge_base.txt
│   ├── inventory_status.json
│   ├── route_options.json
│   └── sample_incidents.json
│
├── src/
│   ├── main.py
│   ├── state.py
│   ├── graph.py
│   ├── nodes.py
│   ├── tools.py
│   ├── rag.py
│   ├── schemas.py
│   └── report_writer.py
│
├── tests/
│   ├── test_tools.py

```

- Data: This folder has the data used as source of truth for this project
- src: It is main folder that contains the agent
- tests: it is used to evaluate tools and nodes

### Setup Instructions


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




### Environment variable setup

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


### Running the Application
```
uv run src/main.py
```
This will run the main agent

###  LangGraph Workflow
 input -> parse incident -> data from db -> get alternative path -> select route -> check for its warehouse -> analyze route -> decision routing -> finalize/ route clarification/ critical delay

finalize-> output save
route clarification-> move to select route
critical delay-> escalate and generate report

###  RAG Implementation
```
Load logistics_knowledge_base.txt
↓
Split the document into chunks
↓
Create embeddings
↓
Store chunks in FAISS
↓
Create a retriever
↓
Retrieve relevant rules
```
### Tools Implemented
There are 2 tools in this project
- query_warehouse_inventory_tool-> This tool is used to get information about warehouse.
- get_alternative_routes_tool-> this tool is used to get available routes

### Testing


