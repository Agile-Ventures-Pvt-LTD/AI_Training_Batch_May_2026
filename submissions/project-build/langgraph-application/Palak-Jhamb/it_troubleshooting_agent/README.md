# Project 03
## Project Title
### IT Troubleshooting Agent with Tool-Using Workflow Using LangGraph
### Submitted By: Palak
### 1. Project overview:
This project is about agentic system with tools and rag system. The goal of this project is to build an IT Troubleshooting Agent that uses LangGraph, Groq, RAG, and custom tools to perform structured diagnosis.
It help  IT support engineers by combining retrieved troubleshooting guidance with tool-based diagnostics.

---

### 2.Setup instructions

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

### 3.Databases
There are 2 databases that are used to respond to user.
1. knowledge_base: it helps to retrieve troubleshooting steps to answer user query
2. database: it is connected with help of tools to answer user query
---

### 4.Environment variable setup

To set any Environment variable, do the following:
1. first create Environment file named **.env**
2. add your api key here 
```python
API_KEY=zws2.....
```
3. Load the api in any folder or file with the help of os
```bash
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['API_KEY'] = os.getenv("API_KEY")
```

---

### 5.How to run  agent

To run the agent run file named as app.py
```bash
python app.py
```
This will run the main application that will end only when user says exit or quit.

---

### 6.Tool list and purpose
There are 7 tools used to respond to user query
1. retrieve_troubleshooting_steps: used to get data from knowledgebase
2.  get_user_profile: use to get information about user
3. get_device_status: use to get information about device
4. check_known_incidents: use to check previous incidents
5. run_diagnostic_check: This tool is used to Return diagnostic snapshot for a user and device
6. get_ticket_details:This tool is used to Fetch existing IT support ticket detail

---

### 7.Sample questions
```
1. Amit says VPN times out after MFA approval. What should we check and what is the next action?
2. Priya's laptop is very slow after startup. Diagnose the likely issue.
3. David cannot login and password reset email is not received. What should be done?
4. Sara's VPN disconnects frequently. What is the likely reason?
5. Outlook is not syncing for Emily but webmail works. What is the next step?
6. Which active known incidents may affect VPN users?
7. Create a ticket summary for Rahul's laptop performance issue.
8. My email is slow. Fix it.
```
---

### 8. Testing

Based on sample queries in PRD , **tests/test.py** is designed.
It runs all sample question provided one by one and save its output at **"outputs"** folder 

- To run Testing file :
```python
python -m tests.test_tools
```

### 9. Final Workflow
1.  LangGraph Pre-built ReAct Agent
```
            user input
                |
               agent
            (need tool)
                |
                /\
       (yes)   /   \  (no)
              /     \   
       Tool call     llm respond by self
            |           |
            \           /
              \       /   
     Repeat until user enter exit or quit
      
```

### 10. Requirements.txt
groq>=1.2.0
ipykernel>=7.3.0
python-dotenv>=1.2.2
tiktoken==0.9.0
pypdf==5.4.0
langchain==0.3.20
langchain-community==0.3.19
langchain-chroma==0.2.2
sentence-transformers==5.1.2
chromadb==0.6.3
langchain-cohere==0.4.5
langchain-groq==0.3.8
langgraph==0.3.21
pillow>=12.2.0
mermaid-python==0.1


 ### 11.How to make vector store


```bash
python database_creation.py
```
This will run the main application that will end only when user says exit or quit.

---