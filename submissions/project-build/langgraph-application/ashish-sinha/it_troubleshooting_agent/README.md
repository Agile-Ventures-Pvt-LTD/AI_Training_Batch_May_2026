# IT Troubleshooting Agent 

## Overview

It is an AI-powered Troubleshooting agentic system built using LangGraph, LangChain, Groq LLM,RAG, and SQLite.

The agent can answer troubleshoot queries by retrieving information from db and knowledge base database through a set of specializes tools as we used in this project.

The project demonstrates:
* Prebuilt ReAct Agent

---

## Tech Stack

* Python 3.12+
* LangChain
* LangGraph
* Groq API
* SQLite
* python-dotenv
* chroma
* HuggingFace
* RAG

---

## Project Structure

```text
it_troubleshooting__agent/
│
├── app.py
├── config.py
├── db_utils.py
├── tools.py
├── prompts.py
├── prebuilt_agent.py
├── graph.py
├── output_parser.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│   └── knowledge_base/
    └── database/
│
├── outputs/
│   ├── evaluation_results.json
```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd it_troubleshooting_agent
```

### 2. Create Virtual Environment

```bash
uv venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```
GROQ_API_KEY= your_groq_api_key
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

## Running the Application

```bash
python app.py
```

---

## Available Tools

1. retrieve_troubleshooting_steps
2. get_user_profile
3. get_device_status
4. check_known_incidents
5. run_diagnostic_check
6. get_ticket_details
7. create_resolution_plan

## Example Queries

```text
These are the questions mentioned in the PRD:
1. Amit says VPN times out after MFA approval. What should we check 
and what is the next action?
2. Priya's laptop is very slow after startup. Diagnose the likely 
issue.
3. David cannot login and password reset email is not received. What 
should be done?
4. Sara's VPN disconnects frequently. What is the likely reason?
5. Outlook is not syncing for Emily but webmail works. What is the 
next step?
6. Which active known incidents may affect VPN users?
7. Create a ticket summary for Rahul's laptop performance issue.
8. My email is slow. Fix it.
```

## Output Example
User Query: My email is slow. Fix it.

Agent Response:
{
        "user_query": "My email is slow. Fix it",
        "parsed_output": {
            "raw_text_answer": "{'messages': [AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'y0c5qa4n7', 'function': {'arguments': '{\"issue_type\":\"VPN\",\"query\":\"user cannot connect to VPN\"}', 'name': 'retrieve_troubleshooting_steps'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 29, 'prompt_tokens': 832, 'total_tokens': 861, 'completion_time': 0.078665241, 'completion_tokens_details': None, 'prompt_time': 0.119888446, 'prompt_tokens_details': None, 'queue_time': 0.050330513, 'total_time': 0.198553687}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_dae98b5ecb', 'service_tier': 'on_demand', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run--019ee00e-2656-7981-bfc1-c1b6de3cbb9e-0', tool_calls=[{'name': 'retrieve_troubleshooting_steps', 'args': {'issue_type': 'VPN', 'query': 'user cannot connect to VPN'}, 'id': 'y0c5qa4n7', 'type': 'tool_call'}], usage_metadata={'input_tokens': 832, 'output_tokens': 29, 'total_tokens': 861}), ToolMessage(content='{\\n  \"issue_type\": \"VPN\",\\n  \"chunks\": [\\n    {\\n      \"source_file\": \"vpn_troubleshooting_guide.md\",\\n      \"chunk_id\": \"chunk_00011\",\\n      \"snippet\": \"# VPN Troubleshooting Guide\\\\n**Document ID:** IT-KB-VPN-001\\\\n**Owner:** IT Network Support\\\\n**Effective Date:** 2026-01-01\\\\n\\\\n## 1. Common Symptoms\\\\nEmployees may report that VPN is not connecting, disconnects frequently, asks for MFA repeatedly, or shows authentication failure.\\\\n\\\\n## 2. First-Level Checks\\\\nBefore escalation, check:\\\\n- Internet connection is active.\\\\n- The user is using the company-approved VPN client.\\\\n- The VPN client version is not older than the minimum supported version: 5.8.\\\\n- System date and time are correct.\\\\n- MFA application is working.\\\\n- The user account is not locked.\\\\n- No known VPN outage is active.\\\\n\\\\n## 3. Authentication Failure\\\\nIf VPN shows authentication failure:\\\\n1. Confirm the user can log in to the company portal.\\\\n2. Check if the user account is locked.\\\\n3. Ask the user to retry MFA approval.\\\\n4. If MFA fails repeatedly, route to Identity Access Management.\"\\n    },\\n    {\\n      \"source_file\": \"vpn_troubleshooting_guide.md\",\\n      \"chunk_id\": \"chunk_00012\",\\n      \"snippet\": \"## 4. Connection Timeout\\\\nIf VPN shows timeout:\\\\n1. Ask the user to switch network, if possible.\\\\n2. Check whether public Wi-Fi is blocking VPN.\\\\n3. Ask the user to restart VPN client.\\\\n4. Check known incidents for VPN gateway outage.\\\\n5. Escalate to Network Support if multiple users are affected.\\\\n\\\\n## 5. Frequent Disconnects\\\\nIf VPN disconnects repeatedly:\\\\n- Check Wi-Fi stability.\\\\n- Ask the user to test with mobile hotspot.\\\\n- Confirm VPN client version.\\\\n- Check device compliance status.\\\\n- Escalate to Endpoint Support if device compliance check fails.\\\\n\\\\n## 6. Escalation Criteria\\\\nEscalate to Network Support when:\\\\n- VPN outage affects multiple users.\\\\n- VPN gateway is unavailable.\\\\n- The user cannot connect from multiple networks.\\\\n- Known incident confirms VPN service degradation.\"\\n    },\\n    {\\n      \"source_file\": \"vpn_troubleshooting_guide.md\",\\n      \"chunk_id\": \"chunk_00013\",\\n      \"snippet\": \"Escalate to Identity Access Management when:\\\\n- MFA failure persists.\\\\n- Account is locked.\\\\n- User cannot authenticate to company portal.\\\\n\\\\n## 7. Safe Response Guidance\\\\nDo not ask users to share passwords, OTPs, MFA codes, private keys, or security tokens.\"\\n    }\\n  ]\\n}', name='retrieve_troubleshooting_steps', id='914f9862-8503-450a-a67e-00a83072c93d', tool_call_id='y0c5qa4n7'), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'c328dw292', 'function': {'arguments': '{\"email\":\"john.doe@example.com\",\"full_name\":\"John Doe\",\"user_id\":\"12345\"}', 'name': 'get_user_profile'}, 'type': 'function'}, {'id': 'b2tgdzacc', 'function': {'arguments': '{\"user_id\":\"12345\"}', 'name': 'get_device_status'}, 'type': 'function'}, {'id': 'sknb4kmwn', 'function': {'arguments': '{\"service_name\":\"VPN\",\"status\":\"active\"}', 'name': 'check_known_incidents'}, 'type': 'function'}, {'id': '7dsabpjdj', 'function': {'arguments': '{\"user_id\":\"12345\"}', 'name': 'run_diagnostic_check'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 92, 'prompt_tokens': 1465, 'total_tokens': 1557, 'completion_time': 0.145715349, 'completion_tokens_details': None, 'prompt_time': 0.076614128, 'prompt_tokens_details': None, 'queue_time': 0.377552921, 'total_time': 0.222329477}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_f8b414701e', 'service_tier': 'on_demand', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run--019ee00e-27b2-79b1-bd97-4d1bcab69ee9-0', tool_calls=[{'name': 'get_user_profile', 'args': {'email': 'john.doe@example.com', 'full_name': 'John Doe', 'user_id': '12345'}, 'id': 'c328dw292', 'type': 'tool_call'}, {'name': 'get_device_status', 'args': {'user_id': '12345'}, 'id': 'b2tgdzacc', 'type': 'tool_call'}, {'name': 'check_known_incidents', 'args': {'service_name': 'VPN', 'status': 'active'}, 'id': 'sknb4kmwn', 'type': 'tool_call'}, {'name': 'run_diagnostic_check', 'args': {'user_id': '12345'}, 'id': '7dsabpjdj', 'type': 'tool_call'}], usage_metadata={'input_tokens': 1465, 'output_tokens': 92, 'total_tokens': 1557}), ToolMessage(content='{\\n  \"found\": false,\\n  \"message\": \"No matching user record found.\"\\n}', name='get_user_profile', id='bee8652f-550b-410c-8c8d-4c1c27e56826', tool_call_id='c328dw292'), ToolMessage(content='{\\n  \"error\": \"No such active registered devices found for user 12345.\"\\n}', name='get_device_status', id='bed8dd20-4b73-4a65-90ac-93839f7e0f49', tool_call_id='b2tgdzacc'), ToolMessage(content=\"Error: ProgrammingError('Incorrect number of bindings supplied. The current statement uses 1, and there are 2 supplied.')\\n Please fix your mistakes.\", name='check_known_incidents', id='16b50a06-98aa-4b53-bdbe-05b6ba71cfe5', tool_call_id='sknb4kmwn', status='error'), ToolMessage(content='{\\n  \"error\": \"Diagnostic generation failed for user 12345.\"\\n}', name='run_diagnostic_check', id='3c805598-db8c-4c62-a625-26b9d0bfaae3', tool_call_id='7dsabpjdj'), AIMessage(content=\"To proceed with the diagnosis, I would like to know the user's identity and the issue they are experiencing. Can you please provide more details about the user and the problem they are facing?\", additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 39, 'prompt_tokens': 1669, 'total_tokens': 1708, 'completion_time': 0.17528979, 'completion_tokens_details': None, 'prompt_time': 0.231340568, 'prompt_tokens_details': None, 'queue_time': 0.049954442, 'total_time': 0.406630358}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_dae98b5ecb', 'service_tier': 'on_demand', 'finish_reason': 'stop', 'logprobs': None}, id='run--019ee00e-2a5a-7f30-8b11-583fb5f1aa97-0', usage_metadata={'input_tokens': 1669, 'output_tokens': 39, 'total_tokens': 1708})]}",
            "status": "Unstructured_Reply"
        }
    }

---

## Output Logs

Agent responses are saved in the following file output directories.

Prebuilt Agent Output Directory:
```text
outputs/evaluation_results.json
```

---

## Security Features

The agent must review the response for unsafe recommendations.
Safety rules:
1. Do not ask for passwords.
2. Do not ask for OTPs.
3. Do not ask for MFA codes.
4. Do not ask users to disable security controls.
5. Do not recommend storing company data in personal drives.
6. Do not expose sensitive user information unnecessarily.

---

## Agent Implementations

### Prebuilt ReAct Agent

Built using:

```python
create_react_agent()
```

---

## Future Enhancements

* Streamlit UI
* FastAPI deployment
* Advanced Graph Routing & State Analytics
* Enhanced RAG Architecture (Advanced Retrieval)
* Security, Compliance, & Guardrail Scaling
* Enterprise Integration & Real-time Data Sync

---

## Author
Ashish Sinha
