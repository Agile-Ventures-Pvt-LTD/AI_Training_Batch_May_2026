# Jira MCP Host Assistant

A simple Jira Issue Assistant built using FastMCP, mcp-use, Groq LLM, and the Jira API. The application allows users to interact with Jira using natural language while the LLM uses MCP tools to retrieve or update Jira data.


# Architecture

Steps:

1. User
2. MCP Host(host.py)
3. Groq LLM
4. Tool Selection
5. MCP Client
6. Jira MCP Server (stdio)
7. Jira REST API
8. Jira Cloud

The user enters a natural language query. The Groq LLM decides which Jira MCP tool should be used. The Jira MCP Server executes the requested operation and returns the result to the host, which generates the final response.


# Project Structure

a006_mcp_host_jira_assistant/

├── server/
│   └── jira_mcp_server.py
│
├── src/
│   ├── host.py
│   ├── llm.py
│   └── prompts.py
|   |__mcp_client.py
|
├── outputs/
│   ├── current_tools.json
│   └── query_history.json
│
├── tests/
├── output_logger.py
├── sample_queries.md
└── README.md

In project Structure , in folders src and server contains __init__.py files which is empty , which are made to make these folders as module.

# Requirements

fastmcp
mcp-use
groq
langchain-groq
python-dotenv
jira
rich
pydantic
pytest

# Jira Configuration

Create a Jira Cloud account and generate an API Token.

Create a `.env` file in the project root.

GROQ_API_KEY=your api key

GROQ_MODEL=llama-3.3-70b-versatile

JIRA_BASE_URL=user base url

JIRA_EMAIL=user email

JIRA_API_TOKEN=user token


# Groq Setup

1. Create a Groq account.
2. Generate an API Key.
3. Add the key to the `.env` file.
4. The project uses:

llama-3.3-70b-versatile


# Running the MCP Server

Start the Jira MCP Server using:

python -m server.jira_mcp_server


The server runs in stdio mode and exposes Jira operations as MCP tools.


# Running the Host

Start the MCP Host using:

python -m src.host

The host performs the following steps:

* Initializes the Groq LLM
* Starts the MCP Client
* Connects to the Jira MCP Server
* Discovers available MCP tools
* Accepts user queries
* Returns the final response
* Response are saved in query_history.json file

Type `exit` to stop the application.

# Running the test cases

for testing run :

pytest -v


# Output Files

The `outputs` folder contains two JSON files.

### current_tools.json

This file temporarily stores the MCP tools used while processing the current user query.
Because host and server are files running in different python processes , so for retrieving "tools_used" for the current query , we are storing the tools used in "current_tools.json" file , and then storing it in "query_history.json"

For example, if the user asks:

Summarize AP-1 including comments


the file may contain:

```json
[
    "get_issue_details",
    "get_issue_comments"
]
'''

Once the response is generated, the file is cleared before processing the next query.


### query_history.json

This file stores the complete history of user queries in the output format specified in the PRD.

Example:

```json
{
    "user_query": "Show open issues",
    "tools_used": [
        "search_issues"
    ],
    "final_answer": "...",
    "write_action_performed": false
}
```

Each new query is appended to the file, creating a structured history of all interactions.


# Sample Queries

* List all Jira projects
* Show open issues
* Show high-priority issues
* Summarize issue AP-1
* Show comments for AP-1
* Show issues assigned to me
* Add a comment to AP-1 saying "QA validation is pending."
* Update the status of AP-1 to In Progress

Replace `AP-1` with a valid issue key from your Jira project.


# Notes

* The mcp_client.py files contains the configuration of connecting it to server , but it is not getting used extensively. So I am using host.py file which contains the configuration also and while running it , it starts the server file.
* All Jira-related queries are answered using MCP tools instead of directly by the LLM.
* Read operations only retrieve information from Jira.
* Write operations, such as adding comments or updating issue status, modify Jira data and are recorded in the output history.
* Tool usage for every query is captured automatically and stored along with the final response.
