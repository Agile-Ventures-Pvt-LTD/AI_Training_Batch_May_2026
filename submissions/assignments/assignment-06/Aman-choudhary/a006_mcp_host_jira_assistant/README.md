# Jira MCP Host Assistant
The objective of this assignment is to build:
1. A Jira MCP Server using FastMCP / mcp-use that runs in stdio mode
2. An MCP Host application that connects to this server
3. An LLM-powered agent using Groq to answer natural language queries 
about Jira issues
## structure.
```
a006_mcp_host_jira_assistant/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── server/
│ └── jira_mcp_server.py
│
├── src/
│ ├── host.py
│ ├── llm.py
│ ├── mcp_client.py
│ ├── prompts.py
│
├── tests/
│
├── outputs/
|____output_logger.py
└── sample_queries.m
```


## Prerequisites

*   Python 3.8+
*   A Jira Cloud instance
*   A Jira API token for authentication

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd a006_mcp_host_jira_assistant
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    Create a `.env` file in the project's root directory and add your Jira credentials:
    JIRA_SERVER=https://your-domain.atlassian.net
    JIRA_USERNAME=your-email@example.com
    JIRA_API_TOKEN=your-jira-api-token
    ```

## Usage

Run the assistant from your terminal:
```bash
python -m src.host.py
```
### Sample Queries
*   List all Jira projects
*   Show open issues
*   Show high-priority issues
*   Summarize issue AP-1
*   Show comments for AP-1
*   Show issues assigned to me
*   Add a comment to AP-1 saying "QA validation is pending."
*   Update the status of AP-1 to "In Progress"