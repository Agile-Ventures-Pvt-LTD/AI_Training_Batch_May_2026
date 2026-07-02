# A006 - MCP Host for Jira Issue Assistant

## Overview

This project implements a **Jira Issue Assistant** using the **Model Context Protocol (MCP)**.

The solution consists of two components:

1. **Jira MCP Server**

   * Built using **FastMCP**
   * Exposes Jira operations as MCP tools
   * Runs in **stdio** mode

2. **MCP Host**

   * Uses the **Groq LLM**
   * Connects to the MCP Server
   * Discovers available tools
   * Executes tool calls
   * Generates natural language responses

---

# Architecture

```
                User
                  │
                  ▼
           src/host.py
                  │
                  ▼
             Groq LLM
                  │
                  ▼
          MCP Client (stdio)
                  │
                  ▼
      server/jira_mcp_server.py
                  │
                  ▼
             Jira REST API
                  │
                  ▼
             Jira Cloud
```

---

# Project Structure

```
a006_mcp_host_jira_assistant/

│── README.md
│── requirements.txt
│── .env.example
│── config.py

├── server/
│   └── jira_mcp_server.py

├── src/
│   ├── host.py
│   ├── llm.py
│   ├── mcp_client.py
│   └── prompts.py

├── tests/
│   ├── test_mcp_server_runs.py
│   ├── test_tool_discovery.py
│   ├── test_query_execution.py
│   ├── test_multi_tool_flow.py
│   └── test_write_operation.py

└── sample_queries.md
```

---

# Technologies Used

* Python 3.12
* FastMCP
* MCP Python SDK
* Groq LLM
* LangChain
* Jira Python SDK
* python-dotenv
* pytest

---

Create a virtual environment.

python -m venv .venv

Activate the environment.

Windows

.venv\Scripts\activate


Install dependencies.

pip install -r requirements.txt

---

# Environment Variables

Create a .env file from .env.example.


GROQ_API_KEY=

GROQ_MODEL=llama-3.3-70b-versatile

JIRA_BASE_URL=https://your-domain.atlassian.net

JIRA_EMAIL=

JIRA_API_TOKEN=



---

# Jira Setup

1. Create a Jira Cloud account.
2. Create a project.
3. Create several dummy issues.
4. Generate a Jira API Token.
5. Update the .env file.

---

# Running the MCP Server

python server/jira_mcp_server.py

The server starts in **stdio mode**.

---

# Running the Host

python src/host.py


Example


You:
Show all open bugs assigned to me.

Assistant:

{
    "user_query": "...",
    "tools_used": [
        "search_issues"
    ],
    "final_answer": "...",
    "write_action_performed": false
}


---

# Available MCP Tools

* list_projects
* search_issues
* get_issue_details
* get_issue_comments
* add_issue_comment
* update_issue_status

---

# Running Tests

Run all tests.


pytest -v


Run a specific test.

pytest tests/test_tool_discovery.py -v


---

# Assignment Requirements Covered

* FastMCP Server
* stdio communication
* Jira Integration
* Groq LLM
* Tool Discovery
* Read Operations
* Write Operations
* Multi-tool Execution
* Pytest
* Documentation

---

# Future Improvements

* Streaming responses
* Better error handling
* Rich CLI interface
* Conversation memory
* Retry mechanism
* Logging
* Tool caching

---

# Author

Vaishnavi Gupta
