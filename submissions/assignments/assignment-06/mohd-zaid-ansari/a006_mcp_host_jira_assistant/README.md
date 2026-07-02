# Jira Issue Assistant

Its an AI powered Jira Assistant build using **FastMCP**, **MCP** which helps you to intract with your Jira Cloud projects and 
let you get all issues, comments from cloud just using Natural language. It use **GroqLLM** for agent to interact with multiple 
mcp tools and helps not to hallucinate.

## 1. Architecture 

The Architecture follows a client-server architecture using **MCP** 

- **Host**(`src/host.py`)
It recieves user query in natural language and coordinate the full flow.

- **GroqLLm**(`src/llm.py`)
It main purpose is to understand the natural language query and decides which tools are required to generate or do the task.

- **MCP Client**(`src/mcp_client.py`)
Its main work is to connect the host and MCP Server using STDIO mode.

- **FastMCP Server**(`server/jira_mcp_server.py`)
It provides all the Jira tools that are required by LLM and Client so to interact with Jira RESTAPI.

# 2. MCP Server Setup

## Install Dependencies

```bash
pip install -r requirements.txt
```

# 3. Jira Configuration

Create a `.env` file in the project root.

```bash
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token
```

Replace the placeholders with your Jira instance details.

# 4. Groq Setup

```bash
GROQ_API_KEY=your-groq-api-key
```

# 5. Running the MCP Server (STDIO)

```bash
python server/jira_mcp_server.py
```

# 6. Running the Host

```bash
python src/host.py
```
The application starts an interactive Jira Assistant.

# 7 Tools Used

- list_projects
- search_issues
- get_issue_details
- get_issue_comments
- add_issue_comment
- update_issue_status

## Project Structure

```text
a006_mcp_host_jira_assistant/
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
├── outputs/
│   └── sample_output.json
│
├── tests/
│   ├── test_mcp_server_runs.py
│   ├── test_tool_discovery.py
│   ├── test_query_execution.py
│   ├── test_multi_tool_flow.py
│   └── test_write_operation.py
│
├── .env.example
├── requirements.txt
└── README.md
```


# 8 Sample Queries

- List all Jira projects
- Show all open high-priority issues
- Summarize issue MCP-2
- Add a comment to MCP-4 saying please solve the problem fast.
- Update issue status of MCP-3 to In Review.


# Output Format

```text
outputs/sample_output.json
```
Example output:

```json
[
    {
        "user_query": "Add a comment to MCP-4 saying please solve the problem fast.",
        "tools_used": [
            "search_issues",
            "get_issue_details",
            "search_issues",
            "search_issues",
            "add_issue_comment"
        ],
        "final_answer": "A comment has been added to MCP-4: \"please solve the problem fast\". \nwrite_action_performed: True \nThe update was successful.",
        "write_action_performed": true
    }
]
```

# Technologies Used

- Python 3.11
- FastMCP
- Model Context Protocol (MCP)
- Groq
- mcp-use
- LangChain
- Requests
- Pytest

### Author

**Mohd Zaid Ansari**



