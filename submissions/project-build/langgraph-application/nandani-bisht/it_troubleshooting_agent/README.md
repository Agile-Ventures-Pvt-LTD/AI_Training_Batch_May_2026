# Project Build: IT Troubleshooting Agent with Tool Using Workflow Using LangGraph

## Overview
An enterprise IT support team receives frequent tickets for issues such as VPN failure, Outlook sync problems, password reset issues, slow laptops, network connectivity problems, and printer access problems.

## Participant Name
Nandani Bisht

## Architecture
```
User Query
 |
 v
Pre-built ReAct Agent
 |
 +--> Issue Classification Tool
 +--> RAG Retrieval Tool
 +--> User Profile Tool
 +--> Device Status Tool
 +--> Known Incident Tool
 +--> Diagnostic Tool
 |
 v
Final Troubleshooting Response
```

## Folder Structure
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
│ ├── knowledge_base/
│ └── database/
│
├── vector_store/
│
└── outputs/
 ├── sample_run_outputs.md
 └── evaluation_results.json
 ```

 ## ## Setup the project


### 1. Create and activate a virtual environment

```bash
uv init
uv venv
venv\Scripts\activate          
```

### 2. Install dependencies

```bash
uv add -r requirements.txt
```

### 3. environment variables

```bash
cp .env.example .env
```
### 4. put documents

it_troubleshooting_agent_dataset.zip
The dataset contains:
data/
├── knowledge_base/
│ ├── vpn_troubleshooting_guide.md
│ ├── email_outlook_troubleshooting_guide.md
│ ├── laptop_performance_guide.md
│ ├── password_reset_guide.md
│ ├── network_connectivity_guide.md
│ └── printer_troubleshooting_guide.md
│
└── database/
 └── it_support.db


 ## 5. Build the vector index

 ## 6. Run the code
 ```
 python app.py
 ```


 ## LangGraph workflow Pattern

## Sequential Pattern
 ```
 User Query
 ↓
Classify Issue
 ↓
Retrieve Troubleshooting Guidance
 ↓
Gather Operational Data
 ↓
Analyze Diagnosis
 ↓
Generate Resolution or Escalation Plan
 ↓
Safety Review
 ↓
Final Answer
```

## Parallelization Pattern
```
Branch 1: Retrieve troubleshooting guide
Branch 2: Get user profile
Branch 3: Get device status
Branch 4: Check known incidents
Branch 5: Run diagnostic snapshot check
```

## 3 Conditional Pattern

### Tools implemented
    
    inspect_database_schema,
    classify_issue_type,
    retrieve_troubleshooting_steps,
    get_user_profile,
    get_device_status,
    check_known_incidents,
    run_diagnostic_check,
    get_ticket_details,
    search_tickets,
    get_active_incidents,


###    Mandatory Test Question

Amit says VPN times out after MFA approval. What should we check and what is the next action?
Priya's laptop is very slow after startup. Diagnose the likely issue.
David cannot login and password reset email is not received. What should be done?
Sara's VPN disconnects frequently. What is the likely reason?
Outlook is not syncing for Emily but webmail works. What is the next step?
Which active known incidents may affect VPN users?
Create a ticket summary for Rahul's laptop performance issue.
My email is slow. Fix it.



