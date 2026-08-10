# IT Troubleshooting Agent

# Participant Name

**Mohd Zaid Ansari**

# Project Overview
The Intelligent IT Troubleshooting Agent is an autonomous service desk companion built using LangChain and ChatGroq. It automates ticket triage, executes system diagnostics, and generates structured resolution plans to dramatically reduce resolution times.Core WorkflowClassification: Parses user queries using an LLM to categorize issues (e.g., VPN, Outlook) and assess diagnostic needs.Parallel Diagnostics: Simultaneously fetches relational account data and hardware health metrics from an SQLite database while querying a Chroma Vector DB for relevant markdown troubleshooting chunks.Synthesis: Combines the diagnostic data with a second LLM layer to output a safe, structured, production-ready resolution plan.

# Setup Instruction
1. Create virtual environmnet
```bash
uv venv
```
2. Activate environment
```bash
.venv/Scripts/activate
```
3.Install Required Libraries
```bash
uv add -r requirements.txt
```
4.Create .env file
```bash
GROQ_API_KEY=...
MODEL_NAME=...
```
# Run The Application
1.Run app.py file
```bash
python app.py
```
# Agent Used
Prebuilt React Agent

# Features
 - Uses tools for different tasks
 - Agent is used to give summarize output
 - Each tools perform different actions
 - Reduce manual lookup everytime
 - Fasten the process of issue solving

# Tech Stack

- Python
- LangGraph
- GroqAPI
- GroqLLM
- Sqlite Database
- RAG

## Project Structure

```text
it_troubleshooting_agent/
│
├── app.py
├── config.py
├── loaders.py
├── retrievers.py
├── db_utils.py
├── tools.py
├── prebuilt_agent.py
├── prompts.py
├── output_parser.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│   ├── knowledge_base/
│   └── database/
│
├── vector_store/
│
└── outputs/
    ├── sample_output.txt
```

# Available Tools

Tools:
- issue_classifiction
- retrieve_troubleshooting_steps
- get_user_profile
- get_device_status
- check_known_incidents
- run_diagnostic_check
- get_ticket_details

# Future Improvements

- Add more tools do get more information.
- Can use multi-agent Collaboration.


# Author

**Mohd Zaid Ansari**