# Enterprise Policy Agentic RAG System

A LangGraph-based Retrieval-Augmented Generation (RAG) system for answering enterprise policy questions using a PreBuilt ReAct Agent.

## Architecture Overview

```
User Query
    ↓
LangGraph PreBuilt ReAct Agent
    ↓
Policy Retrieval Tools (5 tools)
    ├── retrieve_hr_policy
    ├── retrieve_travel_policy
    ├── retrieve_reimbursement_policy
    ├── retrieve_it_security_policy
    └── retrieve_ai_usage_policy
    ↓
Vector Store (Chroma)
    ↓
Policy Documents (./data/policies/)
    ↓
Structured Answer + Evidence + Sources + Confidence
```

## Project Structure

```
enterprise_policy_agentic_rag/
├── app.py                  # Main entry point
├── config.py              # Configuration settings
├── loaders.py             # Document loading
├── chunking.py            # Document chunking
├── retrievers.py          # Vector store setup
├── tools.py               # Tool definitions
├── prompts.py             # System prompts
├── prebuilt_agent.py      # LangGraph ReAct agent
├── graph.py               # Graph structure (minimal)
├── output_parser.py       # Output formatting
├── requirements.txt       # Dependencies
├── data/
│   └── policies/          # Policy markdown files
├── vector_store/          # Persistent Chroma database
└── README.md              # This file
```


## Setup Instructions

### 1. Install Dependencies
```bash
uv pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
```

### 3. Add Policy Documents
Place markdown policy files in `./data/policies/`:
- `ai_usage_policy.md`
- `hr_leave_policy.md`
- `it_security_policy.md`
- `reimbursement_policy.md`
- `travel_policy.md`

### 4. Run the Application
```bash
python app.py
```

## System Features

### 1. Document Processing Pipeline
- **Loading**: Reads markdown files with TextLoader
- **Chunking**: Splits documents into 800-char chunks with 100-char overlap
- **Metadata**: Preserves source file, policy domain, and chunk IDs

### 2. Vector Storage
- **Database**: Chromadb with persistent storage
- **Embeddings**: HuggingFace's `all-MiniLM-L6-v2` model
- **Search**: Cosine similarity with k=3 neighbors

### 3. ReAct Agent
- **Framework**: LangGraph PreBuilt ReAct Agent
- **LLM**: ChatGroq (llama-3.1-8b-instant)
- **Tools**: 5 retrieval tools for different policy domains

### 4. Output Formatting
Returns structured response with:
- **Answer**: Direct answer to the question
- **Supporting Evidence**: Extracted from documents
- **Sources**: Citations with file names and chunk IDs
- **Confidence**: High / Medium / Low confidence level

## Tool Definitions

### 1. `retrieve_hr_policy`
Search and return information about HR leave policy, benefits, and employee management.

### 2. `retrieve_travel_policy`
Search and return information about travel policy, reimbursement, and approval process.

### 3. `retrieve_reimbursement_policy`
Search and return information about reimbursement policy and expense guidelines.

### 4. `retrieve_it_security_policy`
Search and return information about IT security policy and data protection requirements.

### 5. `retrieve_ai_usage_policy`
Search and return information about AI usage policy and guidelines.

## Agent Execution Flow

```
1. User submits query
2. ReAct Agent analyzes query
3. Agent selects appropriate retrieval tool(s)
4. Tool retrieves relevant policy chunks
5. Agent grades retrieved context for relevance
6. If relevant: Generate grounded answer
7. If not relevant: Retry with different tool
8. Format response with evidence and sources
9. Return structured output
```

## Configuration Options

Edit `config.py` to customize:

```python
# LLM Settings
LLM_MODEL = "llama-3.1-8b-instant"
LLM_TEMPERATURE = 0
LLM_MAX_RETRIES = 2

# Document Processing
CHUNK_SIZE = 800       
CHUNK_OVERLAP = 100     
SEARCH_K = 3            

# Vector Store
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_STORE_PATH = "./vector_store"
```

## Example Questions

```
"What is the travel approval process?"
"How much can I be reimbursed for meals?"
"What are the IT security requirements?"
"Can I use ChatGPT at work?"
"What leave options are available?"
```

## Notes

- The system uses **LangGraph's PreBuilt ReAct Agent** (simple, no custom routing)



## Future Enhancements

- [ ] LLM-based context grading
- [ ] Query rewriting with LLM
- [ ] Multi-turn conversation history
- [ ] Answer verification
- [ ] Policy document versioning
- [ ] Web interface
