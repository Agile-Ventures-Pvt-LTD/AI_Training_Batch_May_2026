# Enterprise Policy Assistant — Agentic RAG using LangGraph

## Overview

This project implements an enterprise-grade policy question-answering assistant using LangGraph's pre-built ReAct agent. The assistant retrieves answers exclusively from indexed policy documents and never generates responses from general model knowledge.

## Participant Name
Nandani Bisht

## Architecture

```
User Question
|
Pre-built LangGraph ReAct Agent
     |
     +--[1]--> retrieve_hr_policy / retrieve_travel_policy /
     |         retrieve_reimbursement_policy / retrieve_it_security_policy /
     |         retrieve_ai_usage_policy
     |
     +--[2]--> grade_context
     |              |
     |              +-- REWRITE_QUERY --> rewrite_query --> retrieve again (max 1 retry)
     |              +-- ASK_CLARIFICATION --> agent asks clarifying question
     |              +-- NOT_FOUND --> policy-not-available response
     |              +-- ANSWER --> continue
     |
     +--[3]--> generate_grounded_answer
     |
     +--[4]--> review_answer_grounding
     |
     v
Final Structured Response with Citations
```

## Folder Structure

```
enterprise_policy_agentic_rag/
├── app.py                  
├── config.py               
├── loaders.py              
├── chunking.py             
├── retrievers.py           
├── tools.py                
├── prebuilt_agent.py       
├── prompts.py              
├── output_parser.py        
├── requirements.txt
├── .env.example
├── data/
│   └── policies/
│       ├── hr_leave_policy.md
│       ├── travel_policy.md
│       ├── reimbursement_policy.md
│       ├── it_security_policy.md
│       └── ai_usage_policy.md
├── vector_store/          
└── outputs/
        ├── sample_run_outputs.md
        └── evaluation_results.json
```


## Setup the project


### 1. Create and activate a virtual environment

```bash
uv init
uv venv
venv\Scripts\activate          
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. environment variables

```bash
cp .env.example .env
```

### 4. put documents

Put your `.md`, `.txt`, or `.pdf` policy files in:

```
data/policies/
```

File names must contain one of these keywords for domain detection:
- `hr_leave_policy` → HR_LEAVE
- `travel_policy` → TRAVEL
- `reimbursement_policy` → REIMBURSEMENT
- `it_security_policy` → IT_SECURITY
- `ai_usage_policy` → AI_USAGE

### 5. Build the vector index

```bash
python app.py index
```

This loads all policy documents, chunks them, generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`, and persists the Chroma vector store to `vector_store/`.


### Interactive chat mode

```bash
python app.py chat
```
Type your question at the prompt. Type `exit` to quit.

### Single question mode

```bash
python app.py chat --question "Can I claim meals for same-day business travel?" --output outputs/evaluation_results.json
```

### Batch mode (for testing all 8 required questions)

Create a file `questions.txt` with one question per line, then:

```bash
python app.py batch --input questions.txt --output outputs/evaluation_results.json
```

## Implementation Choice

This project uses the **LangGraph Pre-built ReAct Agent**.

The agent is created using `langgraph.prebuilt.create_react_agent` with a bound LLM (ChatGroq) and 7 custom tools. The agent autonomously decides which tools to call, in what order, and when to stop based on the system prompt instructions and tool descriptions.

---

## LangGraph Workflow Patterns

### Sequential Pattern

Every question follows this ordered chain:

```
Retrieve → Grade Context → (optional: Rewrite + Re-retrieve) → Generate Answer → Review Grounding → Final Response
```

The agent cannot skip retrieval to answer directly. The system prompt enforces this order, and `generate_grounded_answer` only produces answers when given retrieved context.

### Parallelization Pattern

For multi-policy questions (e.g., international travel involving travel + reimbursement + HR approval), the agent calls multiple retrieval tools in sequence and accumulates all chunks before calling `grade_context`. The `retrieve_across_domains` function in `retrievers.py` also merges and re-ranks chunks by relevance score when called directly.

Example: "Can I use customer data in a public AI tool while working remotely?" triggers:
- `retrieve_ai_usage_policy`
- `retrieve_it_security_policy`

Both sets of chunks are passed together into `grade_context` and `generate_grounded_answer`.

### Conditional Pattern

Implemented via the `grade_context` tool's decision field and the agent's system prompt rules:

| Decision | Action |
|---|---|
| ANSWER | Proceed to generate_grounded_answer |
| REWRITE_QUERY | Call rewrite_query once, retrieve again |
| ASK_CLARIFICATION | Ask user a clarifying question, stop |
| NOT_FOUND | Return policy-not-available response |

The one-retry cap on `REWRITE_QUERY` prevents infinite loops (enforced in system prompt: "Only retry once").

---

## Hallucination Control Strategy

1. All prompts instruct the LLM to answer only from retrieved context.
2. `generate_grounded_answer` receives only the retrieved chunks, not general context.
3. `review_answer_grounding` explicitly checks every claim against the context and flags unsupported ones.
4. The agent system prompt explicitly prohibits inventing policy rules.
5. Approval outcomes are never guaranteed — the assistant always defers to manager/finance review.
6. `NOT_FOUND` and `PARTIALLY_ANSWERED` states are returned when context is insufficient.

---

## Tools Implemented

Tool -> Purpose 
`retrieve_hr_policy` | Retrieves HR leave policy chunks |
`retrieve_travel_policy` | Retrieves travel policy chunks |
`retrieve_reimbursement_policy` | Retrieves reimbursement policy chunks |
`retrieve_it_security_policy` | Retrieves IT security policy chunks |
`retrieve_ai_usage_policy` | Retrieves AI usage policy chunks |
`rewrite_query` | Rewrites weak queries for better retrieval |
`generate_grounded_answer` | Generates structured answer from retrieved context only |
`review_answer_grounding` | Verifies answer is supported by retrieved evidence |


     
## Dataset

Policy documents are stored in `data/policies/` as `.md` files. Each file covers one policy domain. Participants should ensure each file contains enough detail to answer the 8 required test questions.

Chunking configuration:
- `chunk_size`: 900 characters
- `chunk_overlap`: 120 characters
- Splitter: `RecursiveCharacterTextSplitter`


Each chunk stores metadata: `chunk_id`, `source_file`, `policy_domain`.


## Known Limitations

1. Parallelization is sequential tool calls within the ReAct loop, not true async parallelism. For true parallel retrieval, the custom LangGraph graph (Choice 2) with `asyncio.gather` would be required.
2. The embedding model runs on CPU. For large policy corpora, switching to a GPU instance will significantly improve indexing speed.
3. The Chroma filter on `policy_domain` requires exact metadata match. If a policy file is named differently, domain detection may fall back to `OTHER` and retrieval will return no results.
4. The ReAct agent's tool call order depends on the LLM's reasoning. The system prompt enforces expected behavior but cannot guarantee exact execution order for every possible query.
5. Context window limits apply. Very large retrieved contexts may be truncated by the Groq model.

## Future Improvements

1. Implement true async parallel retrieval using the custom LangGraph graph.
2. Add a Streamlit UI for non-technical HR and finance staff.
3. Add a feedback loop so employees can mark answers as helpful or incorrect.
4. Support PDF with page-level citation links.
5. Add conversation memory for multi-turn policy Q&A sessions.
6. Add a compliance review mode that logs all queries and responses for audit.
