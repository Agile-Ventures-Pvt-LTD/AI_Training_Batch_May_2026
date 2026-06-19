## Troubleshooting Agent with Tool-Using Workflow Using LangGraph

## SETUP
FOLDER STRUCTURE:
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
 
1. Create virtual environment `uv venv`
2. Install dependencies:
```bash
 uv pip install -r requirements.txt
```

3. Create `.env` file with your Groq API key:

GROQ_API_KEY=------your api key
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
KB_DATA_PATH=data/knowledge_base
VECTOR_STORE_PATH=vector_store
CHUNK_SIZE=900
CHUNK_OVERLAP=120
TOP_K=5
DB_PATH=data/database/it_support.db


5. Run the application:

```bash
uv python app.py
```
## DATASET


```text
data/knowledge_base/
├── vpn_troubleshooting_guide.md
├── email_outlook_troubleshooting_guide.md
├── laptop_performance_guide.md
├── password_reset_guide.md
├── network_connectivity_guide.md
└── printer_troubleshooting_guide.md

data/database/
└── it_support.db
```

## Database Tables

```text
users
devices
tickets
known_incidents
diagnostic_snapshots
```

## tool list
- classify_issue_type,
- retrieve_troubleshooting_steps,
- get_user_profile,
- get_device_status,
- check_known_incidents,
- run_diagnostic_check,
- create_resolution_plan

## sample question 
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

## how to run

```bash
python app.py
```
## Known Limitations

1. Single retry loop for query rewriting
2. No streaming response
3. No web UI 


## Future Improvements
1. Add Streamlit/Gradio web interface
2. Implement conversation memory for follow-up questions
