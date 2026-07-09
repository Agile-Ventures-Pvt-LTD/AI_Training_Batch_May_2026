## IT Troubleshooting Agent with ToolUsing Workflow Using LangGraph
An enterprise IT support team receives frequent tickets for issues such as VPN 
failure, Outlook sync problems, password reset issues, slow laptops, network 
connectivity problems, and printer access problems.
In a real enterprise setup, support agents usually check:
1. Troubleshooting knowledge-base articles
2. User profile
3. Device health
4. Account status
5. Known incidents
6. Diagnostic results
7. Existing support ticket details
## Business Problem
IT support teams face the following challenges:
1. Repetitive troubleshooting questions.
2. Manual lookup of device/user/incident data.
3. Inconsistent escalation decisions.
4. Slow diagnosis for common issues.
5. Unsafe handling of passwords, OTPs, and MFA information.
6. Poor ticket summaries.
7. Lack of structured diagnostic flow.
8. Difficulty combining knowledge-base guidance with operational tool data.
## Dataset 
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

 ##  Folder Structure

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
## Environment Variables
.env.example:
GROQ_API_KEY=########
GROQ_MODEL=llama-3.3-70b-versatile
DB_PATH=data/database/it_support.db
KB_PATH=data/knowledge_base
VECTOR_STORE_PATH=vector_store
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=900
CHUNK_OVERLAP=120
TOP_K=4

## Activate Environment

Git Bash

bash
uv venv
source .venv/Scripts/activate
uv pip install -r requirements.txt
## tested question 
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
8. My email is slow. Fix it
