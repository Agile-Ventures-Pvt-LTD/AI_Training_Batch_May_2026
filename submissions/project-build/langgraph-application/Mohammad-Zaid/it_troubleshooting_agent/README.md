# Enterprise Policy Agentic RAG System

A LangGraph-based Retrieval-Augmented Generation (RAG) system with SQL Tools for answering enterprise Issue questions using a PreBuilt ReAct Agent.

## Architecture Overview

```
User Question
    ↓
ReAct Agent (LLM + Groq)
    ↓
7 Tools:
  ├─ retrieve_troubleshooting_steps → KB Retriever
  ├─ get_user_profile → SQL: users table
  ├─ get_device_status → SQL: devices table
  ├─ check_known_incidents → SQL: known_incidents table
  ├─ run_diagnostic_check → SQL: diagnostic_snapshots table
  ├─ get_ticket_details → SQL: tickets table
  └─ create_resolution_plan → Combines all
    ↓
Response
```

## Project Structure

```
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
│ ├── it_security_policy.md
│ └── ai_usage_policy.md
│
├── vector_store/
│
└── outputs/
 ├── sample_run_outputs.md
 └── evaluation_results.json
```


## Setup Instructions

### 1. create Virtual Environment
```bash
uv venv
```

### 2. Install Dependencies
```bash
uv pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
```
### Add the documents in /data/knowledge_base
6 Documents in the KB 

### 4. Run the Application
```bash
python app.py
```

## System Features

### 1. Document Processing Pipeline
- **Loading**: Reads markdown files with TextLoader
- **Chunking**: Splits documents into 900-char chunks with 120-char overlap
- **Metadata**: Preserves source file, policy domain, and chunk IDs

### 2. Vector Storage
- **Database**: Chromadb with persistent storage
- **Embeddings**: HuggingFace's `all-MiniLM-L6-v2` model (Didn't run due to import issue already discussed)
- **Search**: Cosine similarity with k=4 

### 3. ReAct Agent
- **Framework**: LangGraph PreBuilt ReAct Agent
- **LLM**: ChatGroq (llama-3.1-8b-instant)
- **Tools**: 7 retrieval tools for different issue retrieval


### 4. Output Formatting
Returns structured response with:
- **Answer**: Direct answer to the question
- **Supporting Evidence**: Extracted from documents
- **Sources**: Citations with file names and chunk IDs


## Tool Definitions

### 1. `retrieve_troubleshooting_steps`
Retrieve troubleshooting steps from knowledge base

### 2. `get_user_profile`
Get user profile and device information

### 3. `get_device_status`
Get device status and compliance information

### 4. `check_known_incidents`
Check for known incidents

### 5. `run_diagnostic_check`
Run diagnostic check on user's device

### 6. `get_ticket_details`
Get ticket details for user

### 7. `create_resolution_plan`
Create resolution plan based on user context and issue

## Agent Execution Flow

```
1. User submits query
2. ReAct Agent analyzes query
3. Agent selects appropriate retrieval tool(s)
4. Tool retrieves issue from database c
5. Retrives relevant chunks from Chromadb
7. If not relevant: Retry with different tool
8. Format response with evidence and sources
9. Return structured output
```

## Notes

- The system uses **LangGraph's PreBuilt ReAct Agent** 
- Due to Embedding Model Issue the project was unable to run else the code is complete.
- I had Issue with sentence-transformer as discussed so the project was not run successfully.



## Future Enhancements

- [ ] LLM-based context grading
- [ ] Query rewriting with LLM
- [ ] Multi-turn conversation history
- [ ] Answer verification
- [ ] Issue document versioning
- [ ] Web interface - Streamlit
