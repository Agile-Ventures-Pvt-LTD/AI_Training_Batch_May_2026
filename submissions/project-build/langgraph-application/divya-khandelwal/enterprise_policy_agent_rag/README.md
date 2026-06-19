#  Enterprise Policy Assistant with Agentic RAG Using LangGraph

### Project Context
Enterprises usually maintain many internal policy documents across HR, travel, 
reimbursement, IT security, data privacy, and AI usage. Employees often struggle to find 
the correct policy section, understand eligibility rules, and determine whether their 
scenario is covered.
A normal chatbot may answer from general knowledge and hallucinate policy details. A 
basic RAG system can retrieve policy content, but it may fail when the question requires:
1. Searching across multiple policies.
2. Deciding whether the retrieved context is relevant.
3. Rewriting weak queries.
4. Asking clarifying questions.
5. Refusing unsupported or speculative answers.
6. Combining multiple retrieved sections into a final answer.
7. Reviewing whether the answer is grounded in policy evidence.
The goal of this project is to build an Agentic RAG Policy Assistant using LangGraph. The 
assistant should not behave like a simple one-step RAG chatbot. It should use a graph based workflow that includes retrieval, grading, conditional branching, parallel retrieval, 
and grounded answer generation.


### Custom LangGraph ReAct Agent
Participants manually build a LangGraph workflow using graph nodes, state, and 
conditional edges.
This option is recommended for participants who want to demonstrate deeper 
understanding of LangGraph.

### Required Nodes
query_classifier_node
parallel_retrieval_node
context_grader_node
query_rewriter_node
answer_generator_node
reflection_node
final_response_node

### Expected Architecture
START
 |
 v
query_classifier_node
 |
 v
parallel_retrieval_node
 |
 v
context_grader_node
 |
 +-- relevant context --> answer_generator_node
 |
 +-- weak context --> query_rewriter_node --> parallel_retrieval_node
 |
 +-- ambiguous query --> clarification_response_node
 |
 v
reflection_node
 |
 v
final_response_node
 |
 v
END

#### Steps for setup for this project

1. creating venv -> uv venv
2. activate venv -> .venv/Scripts/activate
3. Install requiremnts -> uv pip install -r requirements.txt

## Folder Structure

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