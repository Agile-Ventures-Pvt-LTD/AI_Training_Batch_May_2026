#  Enterprise Policy Assistant with Agentic RAG

I have used various tools to help the organisation to maintain internal policy and get relevant information about the policies.

# Overview

Enterprises usually maintain many internal policy documents across HR, travel, reimbursement, IT security, data privacy, and AI usage. Employees often struggle to find the correct policy section, understand eligibility rules, and determine whether their scenario is covered. 

# Goal

The goal of this project is to build an Agentic RAG Policy Assistant using LangGraph. The assistant should not behave like a simple one-step RAG chatbot. It should use a graph based workflow that includes retrieval, grading, conditional branching, parallel retrieval, and grounded answer generation. 


# Business Problem 

Employees ask policy questions such as: 
- Can I claim meals during same-day business travel? 
- Can I upload customer data to a public AI tool? 
- What approvals are needed for international travel? 

Currently, employees may: 
1. Search manually across multiple documents. 
2. Misinterpret policy rules. 
3. Ask HR or Finance repeatedly. 
4. Receive inconsistent answers. 
5. Make unsupported assumptions. 
6. Miss required approvals or documentation. 

The proposed assistant should help employees find policy-backed answers quickly and safely.


# Product Goal 

Build an Enterprise Policy Assistant that can: 
1. Load multiple enterprise policy documents. 
2. Chunk and index policy documents. 
3. Retrieve relevant policy sections. 
4. Classify the user query. 
5. Search across multiple policy domains. 
6. Grade whether retrieved context is relevant. 
7. Rewrite the query if retrieval is weak. 
8. Ask clarification if the user’s question is ambiguous. 
9. Generate a grounded answer with citations. 
10. Review whether the final answer is supported by policy evidence. 
11. Demonstrate LangGraph workflow patterns: 

o Sequential Pattern 
o Parallelization Pattern 
o Conditional Pattern 

12. Demonstrate either: 
o LangGraph pre-built ReAct agent, or 
o Custom LangGraph ReAct-style agent. 

# Target Users 

Primary User : Employee 

A user who wants quick policy guidance. 

Secondary User : HR / Finance / IT Support Team 

Teams that repeatedly answer policy-related questions. 

Optional User : Compliance or Risk Reviewer 

A user who wants evidence-backed answers and safe handling of sensitive policy topics.


#  LangGraph Pre-built ReAct Agent 
Participants use a LangGraph pre-built ReAct agent and provide custom tools. This option is recommended for participants who want to focus on: 
1. Tool design. 
2. Retrieval tools. 
3. Context grading tools. 
4. Answer generation. 
5. Policy-safe response generation.

The pre-built agent should be able to call tools such as: 
- retrieve_hr_policy 
- retrieve_travel_policy 
- retrieve_reimbursement_policy 
- retrieve_it_security_policy 
- retrieve_ai_usage_policy 
- grade_retrieved_context 
- rewrite_query 
- generate_grounded_answer

# Custom LangGraph ReAct Agent 
Participants manually build a LangGraph workflow using graph nodes, state, and conditional edges. This option is recommended for participants who want to demonstrate deeper understanding of LangGraph. 

## Required Nodes 
- query_classifier_node 
- parallel_retrieval_node 
- context_grader_node 
- query_rewriter_node 
- answer_generator_node 
- reflection_node 
- final_response_node

#  LangGraph Workflow Patterns 
##  Sequential Pattern 

The assistant must perform a multi-step workflow in sequence.

## Parallelization Pattern 

The assistant must search multiple policy domains in parallel or simulated parallel. 

Required parallel retrieval branches: 
- HR Policy Retriever 
- Travel Policy Retriever 
- Reimbursement Policy Retriever 
- IT Security Policy Retriever 
- AI Usage Policy Retriever 

The graph should merge retrieved results and rank the evidence.


##  Conditional Pattern 

The assistant must branch based on context relevance, query type, or ambiguity. 

Required conditional logic: 

If context is relevant: 
Generate answer 

If context is weak: 
Rewrite query and retrieve again 

If query is ambiguous: 
Ask clarification 

If query is unsupported or speculative: 
Return NOT_FOUND or policy-not-available response 

If answer is not grounded: 
Revise or return insufficient-evidence response

# Functional Requirements
FR-1: Document Loading 

FR-2: Document Chunking 

FR-3: Embeddings and Vector Store 

FR-4: Query Classification

FR-5: Policy Retrieval 

FR-6: Parallel Retrieval

FR-7: Context Grading 

FR-8: Query Rewriting

FR-9: Clarification Handling 

FR-10: Grounded Answer Generation

FR-11: Source Citations

FR-12: Answer Reflection 

FR-13: Final Response 


# Suggested Graph State 

For custom LangGraph implementation, participants may use a state object similar to: 
from typing import TypedDict, List, Dict, Optional 
``` python
class PolicyAgentState(TypedDict): 
user_question: str 
query_type: str 
required_policy_domains: List[str] 
rewritten_query: Optional[str] 
retrieved_context: List[Dict] 
context_grade: Dict 
answer: Dict 
reflection: Dict 
retry_count: int 
final_response: str 
```

#  Suggested Custom Graph Nodes
Node 1: Query Classifier

Node 2: Parallel Retrieval 

Node 3: Context Grader 

Node 4: Query Rewriter

Node 5: Answer Generator 

Node 6: Reflection Node

Node 7: Final Response Node


#  Required Conditional Edges 

```python
After query_classifier_node: 
if requires_clarification == true -> clarification_response_node 
else -> parallel_retrieval_node 
After context_grader_node: 
if decision == ANSWER -> answer_generator_node 
if decision == REWRITE_QUERY and retry_count < 1 -> query_rewriter_node 
if decision == ASK_CLARIFICATION -> clarification_response_node 
if decision == NOT_FOUND -> final_response_node 
After reflection_node: 
if needs_revision == true -> answer_generator_node or final_response_node 
with caveat 
else -> final_response_node
```

# Expected Behavior for Sample Questions 
Question 1 

How many annual leave days can an employee carry forward? 

Expected behavior: 

Retrieve HR leave policy. 

Answer based on carry-forward rule. 

Cite HR policy source.


Question 2 

Can I claim meals for same-day domestic business travel?

Expected behavior: 

Retrieve travel policy and reimbursement policy. 

Explain same-day travel eligibility and meal reimbursement limit if provided. 

Mention receipt requirement if policy says so. 

Do not invent amounts if not present. 


#  Expected Final Output Example

User question: 

Can I claim meals for same-day domestic business travel? 

Expected output shape: 

```python
{ 
"answer": "Based on the retrieved travel and reimbursement policy sections, 
same-day domestic business travel may be eligible for meal reimbursement if 
the trip meets the policy conditions and valid receipts are submitted. The 
claim should follow the reimbursement limits defined in the policy. If the 
policy does not specify the exact amount for your scenario, finance review is 
required.", 
"policy_basis": [ 
"Travel policy mentions same-day business travel eligibility.", 
"Reimbursement policy mentions meal reimbursement and receipt 
requirements." 
], 
"sources": [ 
{ 
"source_file": "travel_policy.md", 
"policy_domain": "TRAVEL", 
"chunk_id": "travel_chunk_003", 
"snippet": "Same-day domestic business travel must be approved by the 
reporting manager..." 
}, 
{ 
"source_file": "reimbursement_policy.md", 
"policy_domain": "REIMBURSEMENT", 
"chunk_id": "reimbursement_chunk_005", 
"snippet": "Meal reimbursement requires valid receipts and must stay 
within the daily policy limit..." 
} 
], 
"answerability": "ANSWERED", 
"confidence": "HIGH", 
"recommended_next_step": "Submit the claim with receipts and manager
approved travel details." 
}
```

# Non-Functional Requirements
NFR-1: Reliability

NFR-2: Security and Privacy 

NFR-3: Maintainability 

#  Technology Stack 

Minimum: 

Python 

LangGraph 

LangChain 

langchain-groq 

Vector store 

Embedding model 

python-dotenv 

Recommended packages: 

langgraph 

langchain 

langchain-core 

langchain-community 

langchain-groq 

langchain-chroma 

chromadb 

sentence-transformers 

python-dotenv 

pydantic 

Optional: 

streamlit 

gradio 

faiss-cpu 

rich 

tabulate 