# ENTERPRISE POLICY AGENTIC RAG

- Enterprise policy agentic RAG is a system developed using RAG, Langchain, LangGraph that answers the queries of users (specially employees) emerging from multiple domains.


## Primary users
- This system is specially designed for employees who have queries about multiple things in the 
office, like queries about leave, using AI, other policies etc.


## Business Objective
- This agentic RAG is very helpful for employees or the corporate people who work in offices
where many policies run together and a heirarchy is maintained.
- Employees find it difficult to asks multiple doubts or queries regarding leaves, IT and many other
parameters.
- Also, visiting HR or any other person in office frequently is very time-taking and inefficient.
- This system is very helpful as it will make this process very smooth and stress free.
- Company policies will be fed to the system and it will answer the user's question as per policies only.


# Choices of Implementation
- Choice 1: Prebuilt - Agent
- Choice 2: Custom - Agent


## Implementation

### Choice 1 : Prebuilt Agent
This option focuses on :
- Tool design.
- Retrieval tools.
- Context grading tools.
- Answer generation.
- Policy-safe response generation.

## Required LangGraph workflow Patterns
There are 3 LangGraph Workflow Patterns.

### Sequential pattern
In this pattern, multiple steps are performed in a sequential pattern.

### Parallelization pattern
Multiple tasks are executed in parallel or simultaneously.

### Conditional Patterns
Tasks are executed on the basis of conditions.
The next path or next move is being decided on the basis of condition(s).
In this case, router is used which lets determine to which node the state will move.


## Virtual environment setup
Install a virtual environment using the command:
cmd:
python -m venv .venv

## Package Requirements
langgraph==0.6.6
langchain==0.3.27
langchain-core==0.3.74
langchain-community==0.3.19
langchain-groq==0.3.7
langchain-chroma==0.2.2
chromadb>=0.6.3
sentence-transformers===5.1.2
python-dotenv==1.1.1
pydantic==2.11.7

These  packages will be installed by the command:
cmd:
pip install -r requirements.txt

## .env setup
Put 
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
POLICY_DATA_PATH=data/policies
VECTOR_STORE_PATH=vector_store
CHUNK_SIZE=900
CHUNK_OVERLAP=120
TOP_K=4

in .env file.

## Folder structure of the project
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
  ├── it_security_policy.md
│ └── ai_usage_policy.md
│
├── vector_store/
│
└── outputs/
 ├── sample_run_outputs.md
 └── evaluation_results.json


## Responsibilities of the files
app.py                             Main entry point
config.py                          Environment variables
loaders.py                         Document loading
chunking.py                        Text splitting
retrievers.py                      Policy retrievers
tools.py                           Tool definitions
graph.py                           Custom LangGraph workflow
prebuilt_agent.py                  Pre-built ReAct implementation
prompts.py                         Prompt templates
output_parser.py                   JSON parsing
README.md                          Setup and usage


## Tasks performed inside the project

### Document Loading
- This is the very first step of this project.
- The document(s) provided is loaded for further processes.

### Document chunking
- Once, the document is being loaded, it is converted into smaller chunks for easy and smooth 
processing.

### Creating Embeddings and vector store
- After creating chunks, these are converted into embeddings (corresponding numerical representations) and being stored in the Vector Database.


### Query classification
- Query is classified on the basis of tools.

### Policy Retrieval
The assistant retrieves policy chunks relevant to the user question.


## How to run the project
Run the command:
cmd:
python app.py

# Author
Vaishnavi Gupta