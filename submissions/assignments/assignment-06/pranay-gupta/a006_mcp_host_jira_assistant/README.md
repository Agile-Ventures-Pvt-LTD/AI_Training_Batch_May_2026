# Jira MCP Host for Jira Issue Assistant

A Jira Issue Assistant built using **FastMCP**, **Groq LLM**, and the **Jira REST API**. The application enables users to interact with Jira using natural language by connecting an MCP Host to a custom Jira MCP Server running in **stdio** mode.

The assistant interprets user requests, selects the appropriate MCP tool, executes the corresponding Jira operation, and returns a clear, natural language response.

---

## Project Overview

This project demonstrates how the **Model Context Protocol (MCP)** can be used to connect a Large Language Model with external tools.

The solution consists of two main components:

- **Jira MCP Server** – Exposes Jira operations as MCP tools.
- **MCP Host** – Uses Groq LLM to understand user queries, invoke the appropriate MCP tool, and generate a final response.

All Jira-related operations are performed through MCP tools instead of allowing the LLM to generate answers directly.

---

## Features

- List available Jira projects
- Search Jira issues using JQL
- View issue details
- View issue comments
- Add comments to Jira issues
- Update issue status
- Natural language query support
- Groq LLM integration
- FastMCP server running in stdio mode
- JSON logging of every interaction
- Unit testing using pytest

---

## Project Structure

```text
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
│   └── prompts.py
│
├── tests/
│   ├── test_mcp_server.py
│   ├── test_mcp_client.py
│   ├── test_llm.py
│   ├── test_tools.py
│   ├── test_host.py
│   └── test_integration.py
│
├── outputs/
│   └── llm_responses.json
│
└── sample_queries.md
```

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Programming Language |
| FastMCP | MCP Server |
| mcp SDK| MCP Host |
| LangChain | LLM Orchestration |
| Groq | Large Language Model |
| Requests | Jira REST API Communication |
| python-dotenv | Environment Variables |
| Pydantic | Data Validation |
| Rich | Console Output |
| Pytest | Testing Framework |

---

## Prerequisites

Before running the project, make sure you have:

- Python 3.11 or later
- A Groq API Key
- A Jira Cloud account
- Jira API Token
- Access to a Jira project with sample issues

---

## Installation

Clone the repository.

```bash
git clone <repository-url>
```

Move into the project directory.

```bash
cd a006_mcp_host_jira_assistant
```

Create a virtual environment.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file using the provided `.env.example`.

```env
GROQ_API_KEY=

GROQ_MODEL=llama-3.3-70b-versatile

JIRA_BASE_URL=https://your-domain.atlassian.net

JIRA_EMAIL=

JIRA_API_TOKEN=
```

---

## Running the MCP Server

Start the Jira MCP Server.

```bash
python server/jira_mcp_server.py
```

The server runs in **stdio mode** and exposes Jira tools to the MCP Host.

---

## Running the MCP Host

Open another terminal and run:

```bash
python src/host.py
```

The application will start an interactive session where you can ask Jira-related questions using natural language.

---

## Supported MCP Tools

The Jira MCP Server exposes the following tools:

- **list_projects** – Lists all available Jira projects.
- **search_issues** – Searches Jira issues using JQL.
- **get_issue_details** – Retrieves detailed information about a specific Jira issue.
- **get_issue_comments** – Retrieves all comments associated with a Jira issue.
- **add_issue_comment** – Adds a new comment to a Jira issue.
- **update_issue_status** – Updates the workflow status of a Jira issue.

---

## Application Workflow

```
User Query
      │
      ▼
MCP Host
      │
      ▼
Groq LLM
      │
      ▼
Tool Selection
      │
      ▼
MCP Client
      │
      ▼
Jira MCP Server
      │
      ▼
Jira REST API
      │
      ▼
Tool Response
      │
      ▼
Groq LLM
      │
      ▼
Final Response
      │
      ▼
Saved to outputs/llm_responses.json
```

---

## Output Format

Each interaction is stored in `outputs/llm_responses.json`.

Example:

```json
{
    "user_query": "Show all open issues",
    "tools_used": [
        "search_issues"
    ],
    "final_answer": "There are 5 open issues in the project.",
    "write_action_performed": false
}
```

---

## Running Tests

Execute all test cases using:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_tools.py
```

---

## Sample Queries

Example queries are available in:

```
sample_queries.md
```

Some examples include:

- List all Jira projects.
- Show all open issues.
- Summarize issue ABC-12.
- Show comments for issue ABC-12.
- Add a comment to ABC-12.
- Move ABC-12 to Done.

---

## Future Improvements

Possible enhancements include:

- Multi-step tool execution
- Automatic transition lookup by status name
- Conversation memory
- Tool result caching
- Rich terminal interface
- Support for additional Jira operations

---

## Assignment Objectives Covered

- FastMCP Server Implementation
- MCP Host Implementation
- Groq LLM Integration
- Jira REST API Integration
- stdio Communication
- Tool Discovery
- Natural Language Query Processing
- Read and Write Jira Operations
- JSON Output Logging
- Unit Testing
- Project Documentation

---
## Author

**Pranay Gupta**