# IT Troubleshooting Agent using LangGraph (Pre-built ReAct Agent)

## Project Overview

In this project we are implementing an enterprise IT Troubleshooting Agent using LangGraph, Groq, Retrieval-Augmented Generation (RAG), and SQLite-based operational tools.

The agent is designed to help IT support engineers diagnose common IT issues such as:

* VPN connectivity failures
* Outlook and email issues
* Password reset and account access problems
* Laptop performance issues
* Network connectivity problems
* Printer access and printing failures

Unlike a traditional chatbot, this agent combines troubleshooting knowledge-base documents with operational support data stored in SQLite. The agent uses tools to retrieve user information, device health, incidents, diagnostics, and ticket details before generating recommendations.

Implementation choice used in this project:

**Choice 1 — LangGraph Pre-built ReAct Agent**

---

# Architecture

```text
User Query
    |
    v
Pre-built ReAct Agent
    |
    +--> classify_issue_type
    |
    +--> retrieve_troubleshooting_steps
    |
    +--> get_user_profile
    |
    +--> get_device_status
    |
    +--> check_known_incidents
    |
    +--> run_diagnostic_check
    |
    +--> get_ticket_details
    |
    +--> create_resolution_plan
    |
    v
Final Troubleshooting Response
```

---

# Features

### Issue Classification

The agent classifies incoming requests into:

* VPN
* OUTLOOK_EMAIL
* LAPTOP_PERFORMANCE
* PASSWORD_RESET
* NETWORK_CONNECTIVITY
* PRINTER
* UNKNOWN

---

### Retrieval-Augmented Generation (RAG)

The agent retrieves troubleshooting guidance from enterprise knowledge-base documents before generating recommendations.

Knowledge sources:

* vpn_troubleshooting_guide.md
* email_outlook_troubleshooting_guide.md
* laptop_performance_guide.md
* password_reset_guide.md
* network_connectivity_guide.md
* printer_troubleshooting_guide.md

---

### SQLite Operational Tools

The agent does not invent operational information.

All user, device, incident, ticket, and diagnostic information is retrieved through tools connected to SQLite.

Database tables:

* users
* devices
* tickets
* known_incidents
* diagnostic_snapshots

---

# Implemented Tools

| Tool                           | Purpose                          |
| ------------------------------ | -------------------------------- |
| classify_issue_type            | Detect issue category            |
| retrieve_troubleshooting_steps | Retrieve KB guidance             |
| get_user_profile               | Fetch user information           |
| get_device_status              | Fetch device health              |
| check_known_incidents          | Retrieve active incidents        |
| run_diagnostic_check           | Retrieve diagnostics             |
| get_ticket_details             | Retrieve support tickets         |
| create_resolution_plan         | Generate recommendations         |
| create_ticket_summary          | Generate support handoff summary |

---

# Sequential Workflow

The project follows the required sequential troubleshooting workflow.

```text
User Query
    ↓
Issue Classification
    ↓
Retrieve Troubleshooting Guidance
    ↓
Gather Operational Context
    ↓
Analyze Evidence
    ↓
Generate Resolution Plan
    ↓
Safety Review
    ↓
Final Response
```

Example:

```text
Priya's laptop is slow

→ Classify issue
→ Retrieve laptop guide
→ Retrieve device status
→ Analyze CPU, memory and disk usage
→ Generate recommendation
→ Escalate if required
```

---

# Parallel Context Gathering

Although the project uses a pre-built ReAct agent, multiple information sources are gathered during reasoning.

Example:

```text
Amit VPN timeout issue

Retrieve VPN guidance
Get user profile
Get device status
Check active incidents
Retrieve diagnostics

Merge evidence

Generate response
```

Context sources are combined before the final recommendation is produced.

---

# Conditional Decision Making

The agent applies conditional logic during troubleshooting.

Examples:

### VPN Issue

```text
Retrieve VPN guide
Check VPN incidents
Review diagnostics
Recommend Network Support if needed
```

### Outlook Issue

```text
Retrieve Outlook guide
Check webmail status
Review diagnostics
Recommend Messaging Support if required
```

### Password Reset Issue

```text
Retrieve password guide
Check account lock status
Check MFA status
Route to IAM
```

### Missing User Information

```text
Ask clarification
```

### High Severity

```text
Recommend escalation
```

---

# Safety Controls

The agent follows enterprise safety requirements.

The agent never:

* Requests passwords
* Requests OTP codes
* Requests MFA codes
* Requests private keys
* Requests security tokens
* Suggests disabling security controls

The agent avoids unsupported root-cause claims when evidence is incomplete.

---

# Project Structure

```text
it_troubleshooting_agent/

├── app.py
├── config.py
├── loaders.py
├── retrievers.py
├── db_utils.py
├── tools.py
├── graph.py
├── prebuilt_agent.py
├── prompts.py
├── output_parser.py
├── requirements.txt
├── .env.example
├── README.md

├── data/
│   ├── knowledge_base/
│   └── database/

├── vector_store/

└── outputs/
    ├── sample_run_outputs.md
    └── evaluation_results.json
```

---

# Installation

Create virtual environment:

```bash
uv venv
```

Activate environment:

Windows:

```bash
.venv\Scripts\activate
```


Install dependencies:

```bash
uv pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key

GROQ_MODEL=llama-3.3-70b-versatile

DB_PATH=data/database/it_support.db

KB_PATH=data/knowledge_base

VECTOR_STORE_PATH=vector_store

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHUNK_SIZE=900

CHUNK_OVERLAP=120

TOP_K=4
```

---

# Running the Application

```bash
python app.py
```

Example:

```text
Enter Issue:

Amit says VPN times out after MFA approval
```

---

# Benchmark Questions Tested

1. Amit says VPN times out after MFA approval. What should we check 
and what is the next action?

2. Priya's laptop is very slow after startup. Diagnose the likely 
issue.

3. David cannot login and password reset email is not received. What 
should be done?

4. Sara's VPN disconnects frequently. What is the likely reason?

5. Outlook is not syncing for Emily but webmail works. What is the 
next step?

6.  Which active known incidents may affect VPN users?

7. Create a ticket summary for Rahul's laptop performance issue.

8. My email is slow. Fix it.


---

# Benchmark Questions Answerd in the .Outputs/ folder

some examples output:

# User Query

Amit says VPN times out after MFA approval. What should we check and what is the next action?

# Agent Response

### We can see the result in better format in terminal but here it looks like this.

{'messages': [HumanMessage(content='Amit says VPN times out after MFA approval. What should we check and what is the next action?', additional_kwargs={}, response_metadata={}, id='132da1e5-cab1-447c-8437-7e429ac3249a'), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'wwgg6yppm', 'function': {'arguments': '{"user_query":"VPN times out after MFA approval"}', 'name': 'classify_issue_type'}, 'type': 'function'}, {'id': 't7qksfcw2', 'function': {'arguments': '{"keyword":"VPN timeout"}', 'name': 'check_known_incidents'}, 'type': 'function'}, {'id': '1cpka6h8d', 'function': {'arguments': '{"user_name":"Amit"}', 'name': 'get_user_profile'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 56, 'prompt_tokens': 1088, 'total_tokens': 1144, 'completion_time': 0.19399249, 'completion_tokens_details': None, 'prompt_time': 0.29966786, 'prompt_tokens_details': None, 'queue_time': 1.137832056, 'total_time': 0.49366035}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_43d97c5965', 'service_tier': 'on_demand', 'finish_reason': 'tool_calls', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019ee001-740d-7330-b484-f648270a5d7e-0', tool_calls=[{'name': 'classify_issue_type', 'args': {'user_query': 'VPN times out after MFA approval'}, 'id': 'wwgg6yppm', 'type': 'tool_call'}, {'name': 'check_known_incidents', 'args': {'keyword': 'VPN timeout'}, 'id': 't7qksfcw2', 'type': 'tool_call'}, {'name': 'get_user_profile', 'args': {'user_name': 'Amit'}, 'id': '1cpka6h8d', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 1088, 'output_tokens': 56, 'total_tokens': 1144}), ToolMessage(content='{"issue_type": "VPN", "confidence": "HIGH", "requires_user_lookup": true, "requires_device_lookup": true, "requires_known_incident_check": true, "requires_clarification": false, "reasoning_summary": "Detected VPN"}', name='classify_issue_type', id='a8c3e178-09aa-4e16-92f4-7a21a4f1ed31', tool_call_id='wwgg6yppm'), ToolMessage(content='{"count": 0, "incidents": []}', name='check_known_incidents', id='5d4e38b6-5c0f-4bef-bf69-af17a535c7eb', tool_call_id='t7qksfcw2'), ToolMessage(content='{"found": true, "user": {"user_id": "USR-1001", "full_name": "Amit Sharma", "email": "amit.sharma@example.com", "department": "Sales", "location": "Pune", "manager": "Neha Rao", "account_status": "Active", "mfa_status": "Enabled"}}', name='get_user_profile', id='b4d7c614-8c79-4a95-964f-4ec7f83d195c', tool_call_id='1cpka6h8d'), AIMessage(content='The issue type is classified as a VPN issue. There are no known incidents related to VPN timeouts. The user profile for Amit has been retrieved, which includes his user ID, full name, email, department, location, manager, account status, and MFA status.\n\nNext, we should retrieve the device status for Amit to check if there are any device-related issues that could be causing the VPN timeout.\n\n', additional_kwargs={'tool_calls': [{'id': 'hednxm7jc', 'function': {'arguments': '{"user_id":"USR-1001"}', 'name': 'get_device_status'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 100, 'prompt_tokens': 1307, 'total_tokens': 1407, 'completion_time': 0.36410203, 'completion_tokens_details': None, 'prompt_time': 0.274421839, 'prompt_tokens_details': None, 'queue_time': 0.050327911, 'total_time': 0.638523869}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_dae98b5ecb', 'service_tier': 'on_demand', 'finish_reason': 'tool_calls', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019ee001-7bf7-7391-9d10-a9a4a12a0b29-0', tool_calls=[{'name': 'get_device_status', 'args': {'user_id': 'USR-1001'}, 'id': 'hednxm7jc', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 1307, 'output_tokens': 100, 'total_tokens': 1407}), ToolMessage(content='{"device_id": "DEV-2001", "user_id": "USR-1001", "device_type": "Laptop", "os": "Windows 11", "compliance_status": "Compliant", "vpn_client_version": "5.9", "disk_free_percent": 22, "cpu_usage_percent": 35, "memory_usage_percent": 62, "last_seen": "2026-06-12 08:45:00"}', name='get_device_status', id='77b2a62e-335e-4dff-ae27-d71986aee4ee', tool_call_id='hednxm7jc'), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'tcv4mk7xb', 'function': {'arguments': '{"user_id":"USR-1001"}', 'name': 'run_diagnostic_check'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 21, 'prompt_tokens': 1433, 'total_tokens': 1454, 'completion_time': 0.043283947, 'completion_tokens_details': None, 'prompt_time': 0.156335026, 'prompt_tokens_details': None, 'queue_time': 0.322699944, 'total_time': 0.199618973}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_ce7bc1685b', 'service_tier': 'on_demand', 'finish_reason': 'tool_calls', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019ee001-7f4e-7a73-a350-715930882100-0', tool_calls=[{'name': 'run_diagnostic_check', 'args': {'user_id': 'USR-1001'}, 'id': 'tcv4mk7xb', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 1433, 'output_tokens': 21, 'total_tokens': 1454}), ToolMessage(content='{"snapshot_id": 1, "user_id": "USR-1001", "device_id": "DEV-2001", "vpn_reachable": 0, "internet_reachable": 1, "webmail_reachable": 1, "internal_apps_reachable": 0, "mailbox_quota_percent": 45, "account_locked": 0, "mfa_push_success": 1, "created_at": "2026-06-12 08:45:00"}', name='run_diagnostic_check', id='ccfe1508-5e65-4839-8fab-0562388d2fde', tool_call_id='tcv4mk7xb'), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'gjzqch1v9', 'function': {'arguments': '{"diagnosis_summary":"VPN timeout after MFA approval for Amit","escalation_required":false,"issue_type":"VPN"}', 'name': 'create_resolution_plan'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 38, 'prompt_tokens': 1567, 'total_tokens': 1605, 'completion_time': 0.085112874, 'completion_tokens_details': None, 'prompt_time': 0.129107255, 'prompt_tokens_details': None, 'queue_time': 0.566546435, 'total_time': 0.214220129}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_ce7bc1685b', 'service_tier': 'on_demand', 'finish_reason': 'tool_calls', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019ee001-81c6-7e52-8578-5f656ec43e71-0', tool_calls=[{'name': 'create_resolution_plan', 'args': {'diagnosis_summary': 'VPN timeout after MFA approval for Amit', 'escalation_required': False, 'issue_type': 'VPN'}, 'id': 'gjzqch1v9', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 1567, 'output_tokens': 38, 'total_tokens': 1605}), ToolMessage(content='{"diagnosis_summary": "VPN timeout after MFA approval for Amit", "recommended_steps": ["Verify internet connectivity", "Confirm VPN client version", "Check active VPN incidents", "Retry using alternate VPN gateway"], "escalation_required": false, "escalation_group": "Network Support", "safety_notes": ["Never ask for password", "Never ask for OTP", "Never ask for MFA code"], "confidence": "HIGH"}', name='create_resolution_plan', id='27058e6b-7e52-497c-87ae-93b34ec2e190', tool_call_id='gjzqch1v9'), AIMessage(content='The issue is related to VPN timeout after MFA approval for Amit. The recommended steps are to verify internet connectivity, confirm VPN client version, check active VPN incidents, and retry using an alternate VPN gateway. No escalation is required at this point. The confidence level in this diagnosis is high.', additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 59, 'prompt_tokens': 1705, 'total_tokens': 1764, 'completion_time': 0.188095772, 'completion_tokens_details': None, 'prompt_time': 0.129629373, 'prompt_tokens_details': None, 'queue_time': 0.321355207, 'total_time': 0.317725145}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_f8b414701e', 'service_tier': 'on_demand', 'finish_reason': 'stop', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019ee001-858e-7781-ac33-2f921a872f17-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 1705, 'output_tokens': 59, 'total_tokens': 1764})]}




# Development Challenges Faced During Implementation

During the implementation of this project, I encountered several practical issues while integrating LangGraph, RAG, SQLite tools, and structured outputs. These challenges helped me better understand the LangChain/LangGraph ecosystem and improve the overall implementation.

## 1. Tool Docstring Error

While creating tools using the `@tool` decorator, I repeatedly encountered a docstring-related error.

The issue occurred because the tool description (docstring) was not placed immediately after the function definition. LangChain expects the docstring to be the first statement inside the function.

Example of the incorrect pattern:

```python
@tool
def get_user_profile(user_name: str):
    query = "..."
    """Fetch user information"""
```

The correct pattern is:

```python
@tool
def get_user_profile(user_name: str):
    """Fetch user information"""
    query = "..."
```

This issue caused tool registration failures until the docstrings were corrected.

---

## 2. Simplifying Resolution Planning Logic

Initially, the resolution planning tool contained multiple nested `if-else` conditions for every issue type.

This made the code difficult to maintain and extend.

To improve readability, I refactored the implementation by storing recommended troubleshooting steps in structured lists and returning them based on the detected issue type. This reduced repetitive conditional logic and made future updates easier.

---

## 3. Output Parser and JSON Formatting Issues

While implementing the output parser, I faced issues where the final response was not being generated in the expected JSON structure.

The root causes included:

* Incorrect variable references.
* Variables being declared but not accessible in the required scope.
* Missing values being passed into the response formatter.

After debugging these issues, I standardized the response structure and ensured consistent output formatting across the project.

---

## 4. Vector Store Implementation Challenges

Setting up the Chroma vector database required additional debugging.

Some of the challenges included:

* Verifying that documents were loaded correctly.
* Ensuring chunks were generated with the correct metadata.
* Confirming embeddings were being created successfully.
* Making sure the vector store persisted locally and could be reloaded on subsequent runs.

Several test runs were required before retrieval results became consistent.

---

## 5. Database Schema Issues

While writing SQLite queries, I initially faced problems caused by incorrect assumptions about table structures and column names.

Some queries failed because the actual database schema differed from what I expected during development.

To resolve this, I inspected the database schema directly and adjusted the queries to match the available tables and columns.

This also led to the creation of helper utilities for database access.

---

## 6. LangGraph Version Compatibility Issues

During development, I encountered compatibility issues related to LangGraph version changes.

Some examples and documentation referenced APIs that had changed in newer releases.

In particular, the pre-built ReAct agent implementation required adjustments to work correctly with the installed LangGraph version.

A significant amount of time was spent validating imports, agent creation methods, and execution behavior.

---

## 7. Output Saving Utility Challenges

While implementing `utils.py`, I faced issues with saving generated responses to the outputs directory.

The main challenges included:

* Creating output folders automatically if they did not exist.
* Generating unique filenames for each execution.
* Ensuring responses were saved correctly without overwriting previous runs.

After several iterations, the utility was updated to automatically create the output directory and save each run with a timestamp-based filename.

---

## Key Learning

This project provided hands-on experience with:

* LangGraph pre-built agents
* Tool-calling workflows
* Retrieval-Augmented Generation (RAG)
* Chroma vector databases
* SQLite integration
* Structured response generation
* Enterprise troubleshooting workflows

Most of the implementation effort was spent on debugging integrations between these components rather than writing the individual modules themselves, which provided valuable practical experience with real-world agent development.




# Known Limitations

* Rule-based issue classification.
* No streaming responses.
* No web-based UI.
* Limited incident correlation logic.
* Retrieval quality depends on KB content.

---

# Future Improvements

* Add custom LangGraph implementation.
* Add Streamlit dashboard.
* Add unit tests.
* Improve issue classification using LLM.
* Add incident severity scoring.
* Add ticket creation workflow.
* Add conversation memory.

---

# Conclusion

This project demonstrates a tool-using IT troubleshooting workflow using LangGraph, Groq, RAG, and SQLite operational data.

The implementation focuses on structured diagnosis, evidence-based recommendations, safe troubleshooting practices, and support-team escalation guidance.
