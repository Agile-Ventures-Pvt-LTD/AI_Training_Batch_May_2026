# IT Troubleshooting Agent with Tool-Using Workflow Using LangGraph
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
The goal of this project is to build an IT Troubleshooting Agent that uses 
LangGraph, Groq, RAG, and custom tools to perform structured diagnosis.
The assistant should not behave like a generic chatbot. It should classify the issue, 
retrieve relevant troubleshooting steps, call tools to inspect operational data, 
branch conditionally based on the issue type and missing information, and 
generate a safe resolution or escalation plan.

### Required Implementation Choices
Participants may choose one of the following:
Choice 1: LangGraph Pre-built ReAct Agent
Choice 2: Custom LangGraph Agent

In this Project, I have used Custom langGraph Agent.

Setup for this Project:
1. create virtual environment -> uv venv
2. Activate virtual environment -> .venv/Scripts/activate
3. Install Requiremnts -> uv pip install -r requirements.txt

### Folder Structure
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


### Custom LangGraph Agent
This option is recommended for participants who want to demonstrate deeper 
graph design.
Expected graph:
START
 |
 v
classify_issue_node
 |
 v
parallel_context_gathering_node
 |
 v
diagnostic_decision_node
 |
 +-- missing information --> clarification_node --> END
 |
 +-- enough information --> resolution_planner_node
 |
 +-- high severity --> escalation_node
 |
 v
safety_review_node
 |
 v
final_response_node
 |
 v
END

### Required custom nodes are as follows:
classify_issue_node
retrieve_kb_node
tool_diagnostics_node
diagnostic_decision_node
resolution_planner_node
safety_review_node
final_response_node

