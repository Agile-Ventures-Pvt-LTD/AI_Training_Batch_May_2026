# Jira Issue Assistant

An intelligent Model Context Protocol (MCP) host application that lets you interact with Jira Cloud using natural language. The project combines FastMCP server tools with Groq's LLM runtime engine to discover, query, update, and manage Jira workflows directly from your terminal while preventing data hallucinations.

---

## 1. Architecture

This application uses a split client-server design where the components talk to each other directly on your machine through standard communication streams. 

Here is what each part of the system does:

* **The Coordinator (`src/host.py`)**  
 It starts up the background server, manages the step-by-step conversation with the LLM, and decides when to use specific tools. Once the work is complete, it saves the final data into structured JSON files.

* **The Messenger (`src/mcp_client.py`)**  
  This component manages the communication hotline. It works quietly in the background, constantly passing messages back and forth without slowing down the rest of the application.

* **The Translator (`src/llm.py`)**  
  This acts as the bridge to the LLM engine. It takes the list of available local tools and translates them into a format that Groq can easily understand and use for tool calls.

* **The Jira Worker (`server/jira_mcp_server.py`)**  
  This connects directly to Jira. It safely interacts with the official Atlassian systems to run tasks, using built-in security filters and error handling to keep the connection stable and safe.


---

## 2. MCP Server Setup

The backend server isolates dependencies and handles downstream requests safely.

### 2.1. Clone Repository

```bash
git clone <repository-url>
cd a006_mcp_host_jira_assistant
```

### 2.2 Dependencies Installation
Create an isolated Python virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2.3 Workspace Directory
```text
a006_mcp_host_jira_assistant/
├── .env
├── requirements.txt
├── README.md
├── sample_queries.md
├── output/
│   └── query_outputs.json
├── server/
│   └── jira_mcp_server.py
└── src/
    ├── host.py
    ├── mcp_client.py
    ├── llm.py
    └── prompts.py
```

---

## 3. Jira Configuration

You must configure these properties inside your root `.env` file:

* **`JIRA_BASE_URL`**: The direct domain URL for your unique cloud instance. Do not include trailing slashes or sub-paths.
* **`JIRA_EMAIL`**: The registered account login email address used to author comments or search issues.
* **`JIRA_API_TOKEN`**: A unique API token generated from your Atlassian security profile.

```bash
JIRA_BASE_URL=https://atlassian.net
JIRA_EMAIL=username@company.com
JIRA_API_TOKEN=your_jira_api_token
```

---

## 4. Groq Setup

* **`GROQ_API_KEY`**: Your unique authorization key provisioned via the Groq Console panel.
* **`GROQ_MODEL`**:  `llama-3.3-70b-versatile`.

### Environment Configuration (`.env`)
```
GROQ_API_KEY=your_groq_api_ey
GROQ_MODEL=llama-3.3-70b-versatile

JIRA_BASE_URL=https://atlassian.net
JIRA_EMAIL=username@company.com
JIRA_API_TOKEN=your_jira_api_token
```

---

## 5. Running Server (stdio)

Start the server using:

```bash
python server/jira_mcp_server.py
```

To test using MCP inspector:

```bash
fastmcp dev server/jira_mcp_server.py
```
---

## 6. Running Host

To run a query, pass your natural language querry argument directly to the host application command line:

```
python src/host.py 
```

### 6.1 Output Logs 
When execution completes, the host prints the unified JSON schema response to your terminal window and automatically saves it to local file storage:

```json
[
  {
    "user_query": "Show all issues",
    "tools_used": [
      "search_issues"
    ],
    "final_answer": "Here are the issues returned by the search:\n\n1. LT-5 - API Error (Status: To Do, Priority: Highest)\n2. LT-4 - MCP Client Development (Status: In Progress, Priority: Highest)\n3. LT-3 - Server Development (Status: In Progress, Priority: High)\n4. LT-2 - ABC-12 (Status: To Do, Priority: Medium)\n5. LT-1 - MCP Learning (Status: To Do, Priority: Highest)\n\nPlease let me know if you would like to view the details of any of these issues or perform any other action.",
    "write_action_performed": false
  },
  {
    "user_query": "List all Jira Projects",
    "tools_used": [
      "list_projects"
    ],
    "final_answer": "Here are the Jira projects available in the connected instance:\n\n1. (Example) Advanced Modeling Techniques - SAM1\n2. AI Team - KAN\n3. Learning Team - LT\n\nLet me know if you need any further assistance.",
    "write_action_performed": false
  },
  {
    "user_query": "Show high-priority issues",
    "tools_used": [
      "search_issues"
    ],
    "final_answer": "Based on the search results, there is one high-priority issue: LT-3, which is currently in progress.",
    "write_action_performed": false
  }
]
```
### 6.2 Running Test Cases
Execute the following shell commands from the project root folder to run the validation framework:

```powershell
# Run the entire test suite with standard coverage indicators
pytest tests/

# Execute verification runs in detailed, verbose logging mode
pytest -v tests/test_jira_assistant.py

# Run verification and allow live console print blocks to stream in real-time
pytest -v -s tests/test_jira_assistant.py
```
---

## 7. Sample Queries

### Read & Write Operations Queries: 

1. Show todo status in Project LT
2. all Jira projects
3. high-priority issues
4. Summarize an issue LT-01
5. how comments for the issue LT-02
6. assigned issues for Ashish Sinha
7. Show all issues
8. Add a comment saying Client.py are successfully created and tested to the issue LT-04
9. Update issue status for LT-03 to Done

---

## 8. Challenges Faced

1. **Python Environment path**: Running the MCP server using sys.executable ensures that dependencies like `fastmcp` are found instead of using global Python to run the server
2. **Transition matching**: Transitioning issue status (update issue status) requires mapping the user's status description (like 'Done') to Jira's internal transition ID, requiring query matching, also modified original system prompt for proper error handling

---

## 9. Future Improvements

* implement Streamlit UI.
* Contextual Conversation History Memory 
* Robust Connection Pools and Automating Retries
* Automated Workflow Schema Validation

### Author
```
Ashish Sinha
```
