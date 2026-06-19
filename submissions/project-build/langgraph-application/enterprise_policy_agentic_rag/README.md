# ENTERPRISE POLICY AGENTIC RAG

## Objective :

Enterprises usually maintain many internal policy documents across HR, travel, reimbursement, IT security, data privacy, and AI usage. Employees often struggle to find the correct policy section, understand eligibility rules, and determine whether their scenario is covered.

A normal chatbot may answer from general knowledge and hallucinate policy details. A basic RAG system can retrieve policy content, but it may fail when the question requires:

1. Searching across multiple policies.
2. Deciding whether the retrieved context is relevant.
3. Rewriting weak queries.
4. Asking clarifying questions.
5. Refusing unsupported or speculative answers.
6. Combining multiple retrieved sections into a final answer.
7. Reviewing whether the answer is grounded in policy evidence.

The goal of this project is to build an Agentic RAG Policy Assistant using LangGraph. The assistant should not behave like a simple one-step RAG chatbot. It should use a graph-based workflow that includes retrieval, grading, conditional branching, parallel retrieval, and grounded answer generation.


## Functionality

1. Document Loading
2. Document Chunking
3. Embeddings and Vector Store
4. Query Classification
5. Policy Retrieval
6. Parallel Retrieval
7. Context Grading
8. Query Rewriting
9. Clarification Handling
10. Grounded Answer Generation
11. Source Citations
12. Answer Reflection
13. Final Response


## Tool Implemented :

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
├── evaluator.py
├── output_schema.py
├── policy_agentic_graph.png
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


## Prebuilt Agent vs Custom LangGraph

In this project, we actually experimented with two approaches: a prebuilt ReAct agent and a fully custom LangGraph workflow. Both are used for different purposes, and honestly each one helped in different parts of the system.


1. Prebuilt Agent (LangGraph ReAct)

We used the prebuilt ReAct agent mainly for quick experimentation and tool-based reasoning.

It basically helps the model decide which tool to call and when, without us manually designing the full graph flow.

Why we used it:
It is very fast to set up.
Handles tool calling automatically
Good for testing retrieval + LLM responses quickly
Reduces boilerplate code


2. Custom LangGraph

The main production pipeline is built using custom LangGraph.

Here we manually design every step like a flowchart:
classification -> retrieval -> grading -> rewriting -> answer generation -> final output

Why we used custom graph:

Full control over execution flow
Easy to implement PRD requirements 

Better handling of edge cases like:

ambiguous questions
weak context
not-found scenarios
We can enforce grounding properly (no hallucination easily)

What it gives us:

Clear multi-step reasoning
Better debugging (each node is visible)
Easier evaluation and scoring integration
More “enterprise style” architecture
Small drawback:
More code and setup compared to prebuilt agent



## Tech Stack

- langchain
- langgraph
- langchain-core
- langchain-community
- langchain-groq
- chromadb
- sentence-transformers
- python-dotenv
- pydantic
- tqdm
- numpy
- langchain-huggingface
- IPython 


## Execution : 

uv run app.py

## Graph

In the folder i also saved a graph image in png format to show the graphical representation of the project flow.

## Outputs

The output are saved in 2 formats -
1. First in md format where query with answer is saved .

2. Second in json format where the expected output as per the PRD.


## Conclusion :

In this project i got hand on experience over the tools like langgraph, langchain, pydantic, Agents, RAG etc.

This project is industry level Enterprise policy agentic RAG that is used to reduce work load and automate various tasks.



