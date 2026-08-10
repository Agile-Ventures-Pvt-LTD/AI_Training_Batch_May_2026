# IT Troubleshooting Agent (LangGraph) Using Prebuilt Agent

A simple LangGraph-based assistant that helps IT support engineers diagnose and resolve common enterprise issues using troubleshooting guides and operational data.

## What this does

Loads troubleshooting documents from local folder  
Creates embeddings and indexes them  
Retrieves relevant troubleshooting steps  
Uses tools to fetch user, device, incident, and ticket data  
Generates structured diagnosis and next actions  
Handles missing information by asking clarification  

## Tech Stack

Python  
LangChain + LangGraph  
HuggingFace embeddings  
Chroma (vector store)  
Groq (LLM)  
SQLite  

## Project Structure

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
│ ├── knowledge_base/
│ └── database/
│
├── vector_store/
│
└── outputs/
 ├── sample_run_outputs.md
 └── evaluation_results.json

## Setup

# create virtual environment
uv venv --python 3.11

# Activate 
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# create .env file
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Run the project using
python app.py

## Sample Query:

# User query:
Amit says VPN times out after MFA approval. What should we check and what is the next action?

# Sample Output:
{
    "timestamp": "2026-06-19 18:06:21",
    "query": "Amit says VPN times out after MFA approval. What should we check and what is the next action?",
    "response": {
      "issue_type": "VPN",
      "diagnosis_summary": "VPN times out after MFA approval for Amit, potential known incident INC-4001 causing VPN gateway latency",
      "evidence_used": {
        "kb_sources": [],
        "tools_used": [
          "check_known_incidents",
          "run_diagnostic_check"
        ],
        "diagnostic_signals": [
          "INC-4001"
        ]
      },
      "recommended_steps": [
        "Verify MFA approval logs",
        "Check VPN gateway latency"
      ],
      "escalation_required": true,
      "escalation_group": "Network Team",
      "safety_notes": [],
      "confidence": "MEDIUM"
    }
}

# outputs
# 1. -> outputs of each query is stored in : outputs/evaluation_results.json
# 2. -> Sample mandatory test query with response are present in : outputs/sample_run_outputs.md

