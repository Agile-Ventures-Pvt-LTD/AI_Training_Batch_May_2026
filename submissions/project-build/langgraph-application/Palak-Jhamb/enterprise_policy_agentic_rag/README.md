# Project-03 
## Project Title
###  Enterprise Policy Assistant with Agentic RAG Using LangGraph
### Submitted By: Palak
### 1. Project overview:
This project is about an AI Assistant that is based on Agentic RAG system.
As enterprises maintain many internal policy documents across various sectors such as HR, travel, 
reimbursement, IT security, data privacy, and AI usage. Employees often struggle to find 
the correct policy section, understand eligibility rules and evaluate whether their scenario is covered or not.
Agentic RAG system act as an assistant that help employees get relevent information and helps to understand if they are eligible or not.
 - it uses RAG system to retrieve relevant data.
 - tools are used to evaluate retrieve context, generate final answer any many more.

 ---
 

### 2. Requirements.txt
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

---


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

### 6.How to make vector store


```bash
python database_creation.py
```
This will run the main application that will end only when user says exit or quit.

---


### 6.How to run agent

To run the agent run file named as app.py
```bash
python app.py
```
This will run the main application that will end only when user says exit or quit.

---

### 7.Sample questions
```
    'How many annual leave days can an employee carry forward?', 
    'Can I claim meals for same-day domestic business travel?', 
    'What documents are needed for hotel reimbursement?', 
    'Can I use my personal laptop for office work?', 
    'What approvals are needed for international travel?',
    'Can customer data be uploaded to a public AI tool?', 
    'Will my reimbursement definitely be approved?',
    'What should I do if the policy does not mention my scenario?'
```

---

### 8. Testing

Based on sample queries in PRD , **tests/test.py** is designed.
It runs all sample question provided one by one and save its output at **"outputs"** folder 

- To run Testing file :
```python
python -m tests.test_tools
```

