# Production-Grade Marketplace RAG Support Agent

The project is to build a RAG based Pydantic Agent chatbot for ShopSphere Marketplace, a platform hosting thousands of independent business sellers a platform hosting thousands of independent business selers.The chatbot must accurately ingestcomplex corporate guidelines—specificaly focusing on advanced business operations, fulfilment strategies, seller ratings, and profitability matrices.

# Setup Instruction
1. Create virtual environmnet
```bash
uv venv
```
2. Activate environment
```bash
.venv/Scripts/activate
```
3.Install Required Libraries
```bash
uv pip install -r requirements.txt
```
4.Create .env file
```bash
GROQ_API_KEY=...
MODEL_NAME=...
```
# Files Description

- **agent.py**: The file is where Pydantic Agent sitting it is used to generate output of user query in Natural Language.
- **config.py**: All the configuration are stored in this file.
- **database.py**: Its has all chunking, loading, retrival and vectorstore functionality
- **guardrails_config.py**: It has all the validation logic like "Profanity Free" and "Toxic Language".
- **prompts.py**: It contains the system message for the our LLM.
- **test.py**: It is the file used to test our all the loading, indexing and chunking are working correctly or not.

# Tool Used 

Only 1 tool is used to get the retrived context from the vector_db to get the relevant context from database.And Agent used to answer from these context.

# Technologies Used

- python
- groq
- guardrails-ai
- pydantic-ai
- RAG
- Langchain

# Features

- Reduces the time of user to get answer from the documents
- User get verified answer from the documents
- Every answer is from pdf sited with reference or page number
- Security is always mainted in the process

## Project Structure

```text
 rag-ecommerce-support-chatbot/ 
├── data/                  
├── chroma_db/             
├── src/                
│   ├── agent.py 
│   ├── guardrails_config.py 
│   └── database.py 
|   |__config.py
|   |__prompts.py
├── tests/               
│   └── test_rag_metrics.py 
├── README.md              
└── requirements.txt  
|__ .env.example
```

# How to Run
```bash
python src.agents.py
```

# Future Imporovment
- Use more tools to make work easy
- Can use Advance RAG Techniques

# Author

**Mohd Zaid Ansari**

