# `A006 - MCP Host for Jira Issue Assistant`

This is a Jira Issue Assistant built with **FastMCP, mcp-use, Groq LLM**, and the **Jira Cloud REST API**.

Here, MCP Host can use a language model to interact with Jira through MCP tools instead of calling the REST API directly.

The application consists of:

- A Jira MCP Server exposing Jira operations as MCP tools
- An MCP Host that connects to the server over stdio


---

# Architecture

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
Tool Response
 ↓
LLM generates answer
```

---

# Project Structure

```
├── .env
├── README.md
├── outputs
│   ├── output.py
│   └── test_output.json
├── pytest.ini
├── .gitignore
├── requirements.txt
├── sample_queries.md
├── server
│   ├── __init__.py
│   ├── config.py
│   ├── jira_client.py
│   └── jira_mcp_server.py
├── src
│   ├── __init__.py
│   ├── host.py
│   ├── llm.py
│   ├── mcp_client.py
│   ├── prompts.py
│   ├── src_config.py
│   └── utils.py
└── tests
    ├── test_host.py
    ├── test_server.py
    └── test_tools.py
```

---

# Environment Variables (Jira and Groq Configuration)

Before running the project, you'll need access to a Jira Cloud workspace and will need to create a Jira Api token. Copy Jira Base URL, Jira Email, Jira Api Token.

Create a Groq account, generate an API key and choose a text generation model of your choice and copy them.

Create a `.env` file in the project root and add the corresponding values.

```env
GROQ_API_KEY=sample_groq_token
GROQ_MODEL=openai/gpt-oss-120b

JIRA_BASE_URL=sample@gmail.com
JIRA_EMAIL=https://sample.atlassian.net
JIRA_API_TOKEN=sample_jira_token
```

---


# Available MCP Tools

The Jira MCP Server exposes the following tools.

| Tool | Description |
|------|-------------|
| list_projects | List all Jira projects |
| search_issues | Search issues using JQL |
| get_issue_details | Retrieve issue details |
| get_issue_comments | Retrieve issue comments |
| add_issue_comment | Add a comment to an issue |
| update_issue_status | Update an issue status |

Communication between the host and server follows stdio transport.

---

# Running the Server (stdio)

Start the Jira MCP Server:

```bash
python server/jira_mcp_server.py
```

The server runs in stdio mode and is intended to be launched by the MCP Host (not directly).

---

# Running the Host

Run the host with:

```bash
python src/host.py
```

During execution, the flow will be: 
MCP Server -> Discover tools -> LLM -> Tool selection -> MCP call -> Response -> Final answer -> store output

Each execution generates a JSON file similar to:

```json
{
    "user_query": "",
    "tools_used": [],
    "final_answer": "",
    "write_action_performed": false
}
```

---

# Running Tests

Run the complete test suite:

```bash
pytest -v
```

Or execute individual test modules:

```bash
pytest tests/test_server.py -v

pytest tests/test_tools.py -v

pytest tests/test_host.py -v
```

---

# Sample Queries

Sample inputs are available in `sample_queries.md`.

Some examples include:

- List all Jira projects
- Show open issues
- Show high-priority issues
- Summarize an issue
- Show issue comments
- Add a comment to an issue
- Update an issue status
- Show issues assigned to me

---

# Features

- Natural language interaction with Jira
- Multi-step tool execution
- Read and write Jira operations
- JSON execution logging
- Pytest-based testING

---

# `THANK YOU`