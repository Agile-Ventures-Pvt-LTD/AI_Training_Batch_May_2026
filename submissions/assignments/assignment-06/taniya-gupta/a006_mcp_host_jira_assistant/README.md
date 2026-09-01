# Assignment 06 - Jira MCP Assistant

This assignment demonstrated learning of MCP server by building a jira assistant that connects an LLM to jira through MCP. It has features like search issues, adding and listing comments and updating issues to jira.
---

## 1. Architecture

- **MCP Server** (`server/jira_mcp_server.py`): Built with `FastMCP`, it registers tools to interact with Jira REST API.
- **MCP Host** (`src/host.py`): Built with `mcp-use` and `langchain-groq`, it runs a loop, handles user queries, invokes the LLM and coordinates the tool execution 

---

## 2. MCP Server Setup

create and activate the venv

---

Install the required dependencies using `uv`:

```bash
uv pip install -r requirements.txt
```

---

## 3. Jira Configuration

configure your `.env` file with Jira credentials:

```ini
JIRA_BASE_URL=https://your-domain.atlassian.net/
JIRA_EMAIL=youremail@example.com
JIRA_API_TOKEN=yourjiraapitoken
```

---

## 4. Groq Setup

Configure your Groq credentials in the same `.env` file:

```ini
GROQ_API_KEY=gsk_your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## 5. Running the Server (stdio)

Start the server using:

```bash
python server/jira_mcp_server.py
```

To test using MCP inspector:

```bash
fastmcp dev server/jira_mcp_server.py
```

---

## 6. Running the Host

Start the host:

```bash
python src/host.py
```

When started the host connects to the Jira MCP server, and runs the assignment through CLI loop. Type "exit" to exit from loop. All query results are saved to `outputs/query_output.json`

---

## 7. Sample Queries

Here are sample queries that I tested on for this assignment:

- **List all Jira projects:**
  > "list all projects"
  > "show all projects"
- **Show open issues:**
  > "show all issues"
  > "show to do issues"
- **Show high-priority issues:**
  > "show high priority issues"
- **Summarize an issue:**
  > "summarize the issue SCRUM-1"
- **Show comments:**
  > "show comments of SCRUM-1"
- **Add a comment:**
  > "Add a comment "New comment added" to SCRUM-1"
- **Update issue status:**
  > "update issue status of SCRUM-1 to done"
- **Show assigned issues:**
  > "show assigned status to me"

---

## 8. Challenges Faced

1. **Python Environment path**: Running the MCP server using sys.executable ensures that dependencies like `fastmcp` are found instead of using global Python to run the server
2. **Transition matching**: Transitioning issue status (update issue status) requires mapping the user's status description (like 'Done') to Jira's internal transition ID, requiring query matching, also modified original system prompt for proper error handling

## 9. Future improvements
- To implement Streamlit UI for better user interaction with the jira assistant

# Author
Taniya Gupta


