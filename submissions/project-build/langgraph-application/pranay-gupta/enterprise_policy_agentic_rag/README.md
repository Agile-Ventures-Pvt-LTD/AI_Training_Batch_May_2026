# Enterprise Policy Assistant with Agentic RAG Using LangGraph
This project is an AI-powered Enterprise Policy Assistant built using LangGraph, Groq LLM, and local document vector stores. 
It allows employees to ask complex corporate policy questions in natural language. 
The agent selects the required policy retrieval and grading tools, extracts relevant information from internal documents, and generates 
evidence-backed, policy-safe responses.

The project contains two implementations:
- Prebuilt ReAct Agent using LangGraph's built-in agent with custom tools
- Custom ReAct Agent built using custom nodes, parallel execution, and grounding reflection

## Features
- Dynamic enterprise query classification
- Multi-policy domain parallel retrieval
- Automated context relevance grading
- Semantic fallback query rewriting
- Missing information clarification routing
- Source-cited grounded answer generation
- Local vector database document indexing
- Hallucination-prevention answer reflection
- Exportable structured JSON system outputs

---
## Tech Stack
- Python
- LangGraph
- LangChain
- Groq LLM
- ChromaDB / FAISS Vector Store

---
## Project Structure
```
enterprise_policy_agentic_rag/
│
├── app.py
├── prebuilt_agent.py
├── graph.py
├── tools.py
├── retrievers.py
├── loaders.py
├── chunking.py
├── prompts.py
├── config.py
├── output_parser.py
├── requirements.txt
│
├── data/
│ └── policies/
│ ├── hr_leave_policy.md
│ ├── travel_policy.md
│ ├── reimbursement_policy.md
│ ├── it_security_policy.md
│ └── ai_usage_policy.md
│
└── outputs/
├── sample_run_outputs.md
└── evaluation_results.json
```

---

## Setup Instructions

1. Create a virtual environment:

```
python -m venv venv
```
Activate environment:

**Windows**
```
venv\Scripts\activate
```


2. Install required packages:

```
pip install -r requirements.txt
```

3. Create a `.env` file and add:

```
GROQ_API_KEY=your_actual_groq_api_token
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
POLICY_DATA_PATH=data/policies
VECTOR_STORE_PATH=vector_store
CHUNK_SIZE=900
CHUNK_OVERLAP=120
TOP_K=4
```

---

## Running the Application
1st Run:
```
python vector_store.py
```

2nd Run:
```
python app.py
```

Enter your policy question. The application will build or load the vector store index, pass the prompt through the agentic graph, display the cited response, and save execution details inside the `outputs` folder.

---

## Available Tools

Tool: 
```
retrieve_hr_policy
retrieve_travel_policy
retrieve_reimbursement_policy
retrieve_it_security_policy
retrieve_ai_usage_policy
grade_context
rewrite_query
generate_grounded_answer
review_answer_grounding
ask_clarification
```

---

## Sample Questions

- How many annual leave days can an employee carry forward?
- Can I claim meals for same-day domestic business travel?
- What documents are needed for hotel reimbursement?
- Can I use my personal laptop for office work?
- What approvals are needed for international travel?
- Can customer data be uploaded to a public AI tool?
- Will my reimbursement definitely be approved?
- What should I do if the policy does not mention my scenario?

---

## Future Improvements

- Add layout-aware chunking for highly complex structural charts in PDF policy documents.
- Enhance custom agent routing thresholds using adaptive human-in-the-loop review nodes.
- Build a lightweight Streamlit web dashboard interface for employee self-service.

---

## Author

Pranay Gupta

