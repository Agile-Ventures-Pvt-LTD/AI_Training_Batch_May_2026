# Assignment Title
## A006: MCP Host for Jira Issue Assistant Using FastMCP / mcp-use and Groq LLM
### Submitted By: Palak
### 1. Project overview:
This assignment is based on MCP which has following component
1. MCP Server- have tools that connects to JIRA Instance
2. MCP Client- client that is used to provide access to server when needed
3. MCP Host- has an agent that is used to respond to user query

---

### 2. Requirements
```
fastmcp>=3.1.0
ipython>=9.10.0
requests>=2.32.5
python-dotenv>=1.2.2
mcp-use>=1.6.0
langchain-groq>=1.1.2
pydantic-ai>=1.78.0
```

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


### 4.Groq setup 

To set any Environment variable, do the following:
1. first create Environment file named **.env**
2. add your api key here 
```python
GROQ_API_KEY=...

```

### 5. Jira configuration
1. open .env file to add data
2. add jira instance data in format below
```
JIRA_BASE_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=
```

---

### 6. Folder structure
```
a006_mcp_host_jira_assistant/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── server/
│   └── jira_mcp_server.py
│
├── src/
│   ├── host.py
│   ├── llm.py
│   ├── mcp_client.py
│   ├── prompts.py
│
├── tests/
│
├── outputs/
│
└── sample_queries.md
```
---
### 6. Architecture
```
User Query
   ↓
MCP Host
   ↓
Groq LLM interprets
   ↓
Tool selection
   ↓
MCP Server call (stdio)
   ↓
Jira API
   ↓
Response
   ↓
LLM generates answer
```

---

### 7. Running server (stdio)

command used to run server 
```
uv run server/jira_mcp_server.py
```

---
### 8.  Running host
To run your host , just type this command in terminal
```
uv run src/host.py
```

---

### 9. How to run test cases
To execute test cases, you need not to run every test case file separately. you can run all test cases sequentially using command below
```
uv run -m pytest -v
```
---

### 10. Sample queries
1. List all Jira projects
2. Show open issues
3. Show high-priority issues
4. Summarize an issue
5. Show comments
6. Add a comment
7. Update issue status
8. Show assigned issues


