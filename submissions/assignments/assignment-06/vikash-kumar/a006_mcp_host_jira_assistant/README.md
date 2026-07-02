#  MCP Host for Jira Issue Assistant 

We have to create MCP host which will be connected to Jira to analyse the issue and give the real time information about the task.

# Objective

The objective of this assignment is to build:
1. A Jira MCP Server using FastMCP / mcp-use that runs in stdio mode
2. An MCP Host application that connects to this server
3. An LLM-powered agent using Groq to answer natural language queries 
about Jira issues

# Business Scenario

A project manager wants to query Jira issues using natural language.

Participants must:
1. Create dummy Jira issues in their own Jira instance
2. Use the MCP server to expose Jira operations
3. Ask questions through the MCP Host

Example queries:
- Show all open high-priority issues.
- Summarize issue ABC-12.
- Which issues are assigned to me?
- What are blockers in the current sprint?
- Show unresolved bugs.
- Add a comment to ABC-5 saying QA validation is pending

# Technology Stack

Minimum required:
- Python
- fastmcp or mcp-use
- Groq LLM
- python-dotenv
- pytest
- pydantic

Recommended:
- langchain-groq
- rich
- pytest-mock


# Environment Variables

```bash
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
JIRA_BASE_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=
```

# Project Structure
```bash
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

# Implementation Flow

```bash
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

# Setup

```python
uv venv

.venv\Scripts\activate

uv pip install -r requirements.txt

```

# File Run

Run this code to run the file

```python
python src/host.py

python -m src.host
```


# Testing

You can run the below code:

```python
pytest tests/ -v
```

# Output Saved

Output willbe saved to the outputs folder by running

```python
python src/host.py
```



# Future Improvement

It can be made more robust with the more tools specific to the different actions.