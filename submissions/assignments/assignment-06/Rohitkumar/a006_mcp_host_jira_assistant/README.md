# A006 - MCP Host for Jira Issue Assistant

An MCP (Model Context Protocol) host application that connects to a Jira MCP server running in stdio mode, powered by Groq LLM for natural language query processing.



## 1. Architecture
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

## 2. MCP Server Setup

### Prerequisites

- Python 3.10+
- Jira Cloud instance with API access
- Groq API key (from [console.groq.com](https://console.groq.com))

### Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:
- `fastmcp` - MCP server framework
- `mcp-use` - MCP client/agent framework
- `groq` / `langchain-groq` - Groq LLM integration
- `python-dotenv` - Environment variable loading
- `requests` - HTTP client for Jira REST API
- `pytest` - Testing framework

### Project Structure

```
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
├── tests/
│   ├── __init__.py
│   └── test_mcp_server.py      
│
├── outputs/                    
├── .env                         
├── .env.example                 
├── requirements.txt
├── sample_queries.md
└── README.md
```

### MCP Server Tools

```
list_projects: List Jira projects
search_issues : Search issues
get_issue_details : Get issue details
get_issue_comments : Get comments
add_issue_comment : Add comment
update_issue_status : Update issue status

---

## 3. Jira Configuration

### Get Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. create the token 

### Configure Environment

Create `.env` file:

```
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_generated_api_token
```



### Create Dummy Issues

You can create test issues in Jira manually 


## 4. Groq Setup

### Get Groq API Key

Create a new API key

### Configure Environment

Add to `.env`:

```
GROQ_API_KEY=gsk_your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```



## 5. Running Server (stdio)

### Start the Jira MCP Server in stdio mode

```bash
python server/jira_mcp_server.py
```



```
Starting MCP server 'Jira MCP Server' with transport 'stdio'
```


## 6. Running Host

The MCP Host automatically starts the Jira MCP Server as a child process and connects to it via stdio.

```bash
python -m src.host
```

You will see:

```
Initializing Jira Issue Assistant...
Connecting to Jira MCP Server via stdio...
Jira Issue Assistant is ready!
Type 'exit' to quit

Enter your query:
```

Type your question and press Enter. The output is a JSON object:

```json
{
  "user_query": "summarize the issue ROH-1",
  "tools_used": ["get_issue_details"],
  "final_answer": "The issue ROH-1 is a task with summary...",
  "write_action_performed": false
}
```


Type `exit` to quit.


## 7. Sample Queries

1. List all Jira projects
2. Show open issues
3. Show high-priority issues
4. Summarize an issue
5. Show comments
6. Add a comment
7. Update issue status
8. Show assigned issues

## Running Tests

```bash
python -m pytest tests/ -v
```


---

## Environment Variables (.env.example)

```
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
JIRA_BASE_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=
```


