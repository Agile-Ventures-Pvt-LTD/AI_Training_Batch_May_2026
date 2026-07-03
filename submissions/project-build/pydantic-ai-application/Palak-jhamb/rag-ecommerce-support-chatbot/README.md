# Project
## Project Build 5 (P005) – Case Study 1: 
## Project Name:Production-Grade Marketplace RAG Support Agent 
### Submitted By: Palak
### Objective:
Modern e-commerce marketplaces require highly available, accurate, and secure automated support for their se ler ecosystems. The goal of this project is to build an enterprise-grade, production-ready Retrieval-Augmented Generation (RAG) chatbot for ShopSphere Marketplace, a platform hosting thousands of independent business selers. 
The chatbot must accurately ingest complex corporate guidelines—specificaly focusing on advanced business operations, fulfi lment strategies, se ler ratings, and profitability matrices. It must answer seler queries instantly while maintaining absolute deterministic safety standards,ensuring no toxic, profane, or ha lucinated outputs are surfaced to end-users. 

### How to do set up
1. initialize uv
```
uv init
```
2. create enviroment
```
uv venv 
```
3. add all requirements
```
uv add -r requirements.txt
```
4. add all api and configrations in **.env** file

5. configure guardrail
```
guardrails configure
```
6. Add profinity free using guardrail hub
```
guardrails hub install hub://guardrails/profanity_free
```


**set-up is complete**

### Requirements.txt
```
groq>=1.2.0
ipykernel>=7.2.0
python-dotenv>=1.2.2
langchain==0.3.20
langchain-community==0.3.19
langchain-chroma==0.2.2
sentence-transformers==5.1.2
chromadb==0.6.3
langchain-cohere==0.4.5
pydantic-ai>=1.21.0
langchain-pymupdf4llm
guardrails-ai>=0.6.7
presidio-analyzer>=2.2.363
presidio-anonymizer>=2.2.363
pymupdf==1.28.0
database-pydantic-ai
```

### How to create database
To create database (1 time process) run command in terminal
```
uv run src.utils.py
```

### How to run project
```
uv run main.py
```

