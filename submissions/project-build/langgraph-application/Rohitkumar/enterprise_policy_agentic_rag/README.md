# Enterprise Policy Assistant with Agentic RAG Using LangGraph

An enterprise policy assistant built with LangGraph, Groq, and LangChain that uses Agentic RAG to answer employee policy questions from HR, Travel, Reimbursement, IT Security, and AI Usage policies.

## Implementation Choice: Custom LangGraph ReAct Agent

This project implements Choice 2: Custom LangGraph ReAct Agent with manually built LangGraph workflow using graph nodes, state, and conditional edges.

## Setup

Folder Structure: 
enterprise_policy_agentic_rag/ 
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
├── data/policies      
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

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
POLICY_DATA_PATH=data/policies
VECTOR_STORE_PATH=vector_store
CHUNK_SIZE=900
CHUNK_OVERLAP=120
TOP_K=5


5. Run the application:

```bash
uv python app.py
```

The application will:
- Load and chunk policy documents from `data/policies/`
- Create embeddings and vector store
- Run all 8 test questions automatically
- Enter interactive mode for custom questions

## Dataset

- hr_leave_policy.md
- travel_policy.md
- reimbursement_policy.md 
- it_security_policy.md 
- ai_usage_policy.md

Documents are chunked and indexed in Chroma vector store using HuggingFace embeddings.

## Graph Design
START > query_classifier >  parallel_retrieval > context_grader > answer_generator > reflection > final_response > END
                                |                  |
                                |            (REWRITE_QUERY > query_rewriter)
                           (AMBIGUOUS > clarification_response >  END)




### Sequential Pattern
The assistant follows a strict sequence: Classify -> Retrieve -> Grade -> Generate -> Reflect -> Respond.

### Parallelization Pattern
For multi-policy questions, the system retrieves from HR_LEAVE, TRAVEL, REIMBURSEMENT, IT_SECURITY, and AI_USAGE domains in parallel, merging results.

### Conditional Pattern
The graph branches based on:
- Query type (clarification needed or not)
- Context relevance (ANSWER, REWRITE, CLARIFY, NOT_FOUND)
- Retry count (max 1 rewrite loop)
- Reflection outcome (needs revision or final)

## Hallucination Control Strategy
1. Grounded generation
2. Context grading 
3. Reflection 
4. NOT_FOUND path
5. Clarification path 
6. Confidence scoring

## Node Descriptions
 1. Query Classifier 
 2. Parallel Retrieval 
 3. Context Grader
 4. Query Rewriter 
 5. Answer Generator
 6. Reflection Node 
 7. Final Response Node  


## Known Limitations

1. Single retry loop for query rewriting
2. No streaming response
3. No web UI 


## Future Improvements
1. Add Streamlit/Gradio web interface
2. Implement conversation memory for follow-up questions
