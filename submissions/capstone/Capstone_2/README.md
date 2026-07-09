# CAPSTONE PROJECT NO.2

## What this is

- Capstone Project 2 is a MCP Based enterprise operations assistant. It allows an engineer to ask a plain-English question and the answer is pulled from three separate operational systems automatically at once.

## Stack Of Choice

FastMCP (servers) · mcp-use (agent/client) · langchain-groq (LLM) · Groq
`llama-3.3-70b-versatile` · Python `json`/`sqlite3` for data access · pytest

## File Structure 

mcp-enterprise-operations-assistant/
├── data/
├── outputs/
├── scripts/
├── servers/
    ├── change_management_server.py
    ├── service_health_server.py
    └── support_ticket_server.py
├── tests/
├── .env.example
├── host.py
├── main.py
├── requirements.txt


## Setup and running it

- Install dependencies
- `python tool_discovery.py` — connects to all three servers live, writes
  out exactly what tools each one exposes.
- `python host.py` — interactive prompt, ask questions one at a time.
- `python main.py` — runs all 8 mandatory questions end-to-end, writes a
  JSON results file and a markdown summary.
- `pytest tests/` — runs the test suite.


## Limitations of How I Built This

- `host.py` is one flat script — no separate config/prompts file, so
  changing the system prompt or server setup means editing the Host
  directly.
- No retry logic — a failed Groq call on a mandatory query is marked
  "FAIL" rather than retried.
- Tool discovery and the Host each define their own server config
  separately, so they could drift out of sync if only one is updated.
- No conversation memory — each question is handled statelessly, so
  multi-turn follow-ups aren't supported.
- Tests only cover the three servers' tool functions directly — no
  pytest-based MCP discovery or live agent integration test yet.

## Where I used AI in This Project 

- I used it for making some of the test cases - namely in making the test cases for testing the servers
- I had tried using AI while making the file run_mandatory_queries.py which was suggested in the Capstone PRD but I was facing errors with it and hence I changed the files to use a simple main.py alongside host.py to run the project.
- I used AI to make some improvements to the README.MD doc while writing it and while formatting it


## Where Some Of The Code Was Inspired From
- The three MCP servers (service_health_server.py, support_ticket_server.py, change_management_server.py)  follow the FastMCP server style from ankur-code-lab/mcp-mastery, specifically the pattern used in the 1_Basic_MCP_Server folder — load_dotenv(), mcp = FastMCP(...), @mcp.tool with docstrings, mcp.run(transport="stdio").

- tool_discovery.py follows the Client + list_tools() connection pattern from the carbon_mcp_server.py / client example in ankur-code-lab/Building-RAG-Agentic-AI-Application (MCP folder), adapted from one HTTP server to looping over three stdio servers.

- host.py's flat, top-level structure (model, client, and agent all built at import time, no wrapper function) follows the same shape as agent_with_mcp.py in that same Building-RAG-Agentic-AI-Application/MCP folder, re-implemented with mcp-use's MCPAgent and langchain-groq instead of pydantic_ai, to stay within the project's required tech stack.

- All of these are from ankur_code_labs repos no outside souces.