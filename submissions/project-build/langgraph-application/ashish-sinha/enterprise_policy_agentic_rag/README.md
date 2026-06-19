#  Enterprise Policy Assistant Agentic RAG  

## Business Problem

Current employees face problem in:
1. Search manually across multiple documents. 
2. Misinterpret policy rules. 
3. Ask HR or Finance repeatedly. 
4. Receive inconsistent answers. 
5. Make unsupported assumptions. 
6. Miss required approvals or documentation.

So, We have to build an Enterpise Policy Assistant that can solve this probems.

## Overview

The project demonstrates two distinct architectural implementations:
**Prebuilt ReAct Agent**: 

LangGraph Pre-built ReAct Agent 
Participants use a LangGraph pre-built ReAct agent and provide custom tools.


Expected Capabilities 
The pre-built agent should be able to call tools such as: 

retrieve_hr_policy 
retrieve_travel_policy 
retrieve_reimbursement_policy 
retrieve_it_security_policy 
retrieve_ai_usage_policy 
grade_retrieved_context 
rewrite_query 
generate_grounded_answer 

Expected Architecture 

User Question 
| 
v 
Pre-built ReAct Agent 
| 
+--> Select Tool 
| 
+--> Retrieve Policy Context 
| 
+--> Grade Context 
| 
+--> Generate Final Answer 
| 
v 
Grounded Answer with Citations


---

## Tech Stack
* **Language**: Python 3.12+
* **Frameworks**: LangChain, LangGraph
* **Inference API**: Groq API
* **Vector Store**: Vector DB
* **Environment Management**: python-dotenv

---

## Project Structure
```text
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
│   └── policies/ 
├── hr_leave_policy.md 
├── travel_policy.md 
├── reimbursement_policy.md 
├── it_security_policy.md 
└── ai_usage_policy.md 
│       
│ 
├── vector_store/ 
│ 
└── outputs/ 
├── sample_run_outputs.md 
└── evaluation_results.json
```

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone <repository-url>
cd enterprise_policy_agentic_rag
```

### 2. Create Virtual Environment
```bash
uv venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv pip install -r requirements.txt
```

---

## Environment Variables
Create a `.env` file in the root directory matching this schema:

```env
GROQ_API_KEY= your_groq_api_key
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
Execute the primary runtime block wrapper:

```bash
python app.py
```

---

## Available Tools

1. retrieve_hr_policy 
2. retrieve_travel_policy 
3. retrieve_reimbursement_policy 
4. retrieve_it_security_policy 
5. retrieve_ai_usage_policy 
6. grade_context 
7. rewrite_query 
8. generate_grounded_answer 
9. review_answer_grounding 
10. ask_clarification

---

## Example Questions
The system is explicitly tuned to handle core requirement constraints defined in the PRD:

1. How many annual leave days can an employee carry forward?
2. How many annual leave days can an employee carry forward?
3. What documents are needed for hotel reimbursement? 
4. Can I use my personal laptop for office work? 
5. What approvals are needed for international travel?
6. What approvals are needed for international travel?
7. What approvals are needed for international travel?
8. What should I do if the policy does not mention my scenario?

---

## Output Example
**User question:** `Can I claim meals for same-day domestic business travel?`

**Agent Response:**
```
{
        "question": "How many annual leave days can an employee carry forward?",
        "response": "{'answer': 'An employee can carry forward a maximum of 6 unused annual leave days into the next calendar year.', 'policy_basis': ['Carry-Forward Rules'], 'sources': ['hr_leave_policy.md'], 'answerability': 'Direct answer from policy', 'confidence': 'High', 'recommended_next_step': 'Review HR Leave Policy (HR-LV-001) for further details on leave entitlement and carry-forward rules.'}"
    },

```

---

## Output Logs
Agent execution outputs are persisted across designated local tracking folders:

* **Prebuilt Engine Context Dump Logs:** `outputs/evaluation_results.json`

---
## Agent Implementations

### Prebuilt ReAct Agent
Instantiated through pre-configured template engines:
```python
create_react_agent()
```
Maintains parity across tools parameters, token metrics targets, and model definitions.

---

## Future Enhancements
* **Streamlit UI**: Front-end visual component interface dashboard web integration.
* **FastAPI Deployment**: High-speed REST backend deployment wrapper.
* **RBAC Controls**: Granular authorization and access control layer validation boundaries.
* **Policy RAG Layer**: Documentation search using vector embeddings databases.
* **Multi-Agent RAG**: Use multi agent based sytem usinf RAG.

---

## Author
**Ashish Sinha**
