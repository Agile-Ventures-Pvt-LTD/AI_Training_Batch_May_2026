# IT Troubleshooting Agent

An enterprise-grade IT support agent powered by LangGraph, Groq LLM, and Retrieval-Augmented Generation (RAG). This agent helps IT support engineers diagnose and resolve technical issues using knowledge base documents and operational data.

## Features

- **RAG-Powered Troubleshooting**: Retrieves relevant troubleshooting guides from a knowledge base
- **Intelligent Tool Use**: Accesses user profiles, device status, known incidents, and diagnostic data
- **Safety-First Design**: Never requests passwords, OTPs, or sensitive credentials
- **Structured Output**: JSON-formatted responses with diagnosis, escalation info, and recommendations
- **Automatic Escalation**: Detects critical issues and routes to appropriate support teams


## Project Structure

```
it_troubleshooting_agent/
│
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
│
├── data/
│   ├── knowledge_base/
│   └── database/
│
├── vector_store/
│
└── outputs/
    ├── sample_run_outputs.md
    └── evaluation_results.json                   
```

## Setup

### 1. Configure Environment

```
cp .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 2. Run the Agent

```
python app.py
```

## Usage

### Interactive Mode

```
Support Query: Amit says VPN times out after MFA approval. What should we check?
```

The agent will:
1. Retrieve relevant troubleshooting steps from the knowledge base
2. Look up user profile and device status
3. Run diagnostics to check connectivity
4. Check for known incidents affecting VPN
5. Return a structured JSON response with diagnosis and next steps

### Test Queries

The agent supports these 8 mandatory test scenarios:
```
1. Amit says VPN times out after MFA approval. What should we check and what is the next action?
2. Priya's laptop is very slow after startup. Diagnose the likely issue.
3. David cannot login and password reset email is not received. What should be done?
4. Sara's VPN disconnects frequently. What is the likely reason?
5. Outlook is not syncing for Emily but webmail works. What is the next step?
6. Which active known incidents may affect VPN users?
7. Create a ticket summary for Rahul's laptop performance issue.
8. My email is slow. Fix it.
```


## Available Tools (7+)

1. retrieve_troubleshooting_steps
2. get_user_profile
3. get_device_status
4. check_known_incidents
5. run_diagnostic_check
6. get_ticket_details
7. create_resolution_plan


## Output Format

All responses are JSON-formatted with these fields:

```json
{
  "issue_type": "VPN",
  "diagnosis_summary": "VPN authentication timeout after MFA",
  "evidence_used": {
    "kb_sources": ["vpn_troubleshooting_guide.md"],
    "tools_used": ["retrieve_troubleshooting_steps", "get_user_profile"],
    "diagnostic_signals": ["vpn_reachable: false", "mfa_push_success: false"]
  },
  "recommended_steps": [
    "Verify MFA push was received",
    "Check VPN client version is current",
    "Clear VPN client cache and retry",
    "If issue persists, run full diagnostic"
  ],
  "escalation_required": true,
  "escalation_group": "Network Support",
  "safety_notes": [
    "Do not request or share MFA codes",
    "Verify user identity before escalation",
    "Document all troubleshooting steps"
  ],
  "confidence": "HIGH"
}
```

## Configuration

Key environment variables in `.env`:
```
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
DB_PATH=data/database/it_support.db
KB_PATH=data/knowledge_base
VECTOR_STORE_PATH=vector_store
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=900
CHUNK_OVERLAP=120
TOP_K=4
```
## Data Sources

### Knowledge Base (6 Guides)
Located in `data/knowledge_base/`:
- Troubleshooting steps for VPN, Email, Laptop, Password, Network, Printer issues
- Markdown formatted with clear sections and instructions

### SQLite Database (5 Tables)

Located at `data/database/it_support.db`:
- **users** 
- **devices**
- **tickets**
- **known_incidents**
- **diagnostic_snapshots**


## Future Enhancements
- Multi-language support
- Integration with ticketing systems (Jira, ServiceNow)
- Feedback loop for continuous improvement
- Advanced analytics dashboard
- Real-time incident correlation
- Automated remediation for common issues
