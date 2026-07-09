## Project Build: Enterprise Policy Assistant with Agentic RAG Using LangGraph

## folder 
enterprise_policy_agentic_rag/
│
├── app.py
├── config.py
├── loaders.py
├── chunking.py
├── retrievers.py
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
│ └── policies/
│ ├── hr_leave_policy.md
│ ├── travel_policy.md
│ ├── reimbursement_policy.md
│ ├── it_security_
│ └── ai_usage_policy.md
│
├── vector_store/
│
└── outputs/
 ├── sample_run_outputs.md
 └── evaluation_results.json


 ## entry point 
 File Responsibility
app.py Main entry point
config.py Environment variables
loaders.py Document loading
chunking.py Text splitting
retrievers.py Policy retrievers
tools.py Tool definitions
graph.py Custom LangGraph workflow
prebuilt_agent.py Pre-built ReAct implementation
prompts.py Prompt templates
output_parser.py JSON parsing
README.md Setup and usage

## ## Activate Environment

Git Bash

bash
uv venv
source .venv/Scripts/activate
uv pip install -r requirements.txt
gemini /settings
## tested question 
            How many annual leave days can an employee carry forward?
            Can I claim meals for same-day domestic business travel?
            What documents are needed for hotel reimbursement?
            Can I use my personal laptop for office work?
            What approvals are needed for international travel?
            Can customer data be uploaded to a public AI tool?
            Will my reimbursement definitely be approved?
            What should I do if the policy does not mention my scenario?
