# Enterprise Policy Assistant (Agentic RAG)

A simple LangGraph-based assistant that answers employee policy questions using internal documents (HR, travel, reimbursement, IT, etc.).

## What this does
Loads policy documents from local folder
Splits and indexes them using embeddings
Retrieves relevant policy sections
Generates answers based only on retrieved content
Handles weak queries and missing context

## Tech Stack
Python
LangChain + LangGraph
HuggingFace embeddings
FAISS / Chroma (vector store)
Groq (LLM)

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
````

## Setup

```bash
# create venv
uv venv --python 3.11
.\.venv\Scripts\activate

# install deps
uv pip install -r requirements.txt
````

Create a `.env` file:

```
GROQ_API_KEY=your_key_here
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## Run

```bash
python app.py
```

## Sample Questions

Can I claim meals for same-day travel?
What approvals are needed for international travel?
Can I use customer data in a public AI tool?

## Sample Output 

{
        "question": "What approvals are needed for international travel?",
        "response": {
            "answer": "Based on the retrieved policy content, relevant guidance has been found.",
            "policy_basis": [
                "For same-day domestic travel:\n- manager approval is required before travel\n- meal reimbursement is governed by the Reimbursement Policy\n- local transp",
                "For same-day domestic travel:\n- manager approval is required before travel\n- meal reimbursement is governed by the Reimbursement Policy\n- local transp",
                "For same-day domestic travel:\n- manager approval is required before travel\n- meal reimbursement is governed by the Reimbursement Policy\n- local transp",
                "For same-day domestic travel:\n- manager approval is required before travel\n- meal reimbursement is governed by the Reimbursement Policy\n- local transp"
            ],
            "sources": [
                {
                    "source_file": "travel_policy.md",
                    "policy_domain": "TRAVEL",
                    "chunk_id": "chunk_0015"
                },
                {
                    "source_file": "travel_policy.md",
                    "policy_domain": "TRAVEL",
                    "chunk_id": "chunk_0015"
                },
                {
                    "source_file": "travel_policy.md",
                    "policy_domain": "TRAVEL",
                    "chunk_id": "chunk_0015"
                },
                {
                    "source_file": "travel_policy.md",
                    "policy_domain": "TRAVEL",
                    "chunk_id": "chunk_0015"
                }
            ],
            "answerability": "ANSWERED",
            "confidence": "HIGH",
            "recommended_next_step": "Review policy citations and follow the approval process where required."
        }
    }

    
## Notes

Answers are based only on policy docs (no guessing)
If info is missing, it will say so instead of making assumptions
Some responses may ask for clarification

## Limitations

Depends on quality of policy documents
Retrieval can miss context in edge cases
No UI (CLI only)

