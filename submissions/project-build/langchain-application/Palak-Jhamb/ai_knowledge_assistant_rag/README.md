## Submitted By

**Name:** Palak Jhamb

---

## Project Name

**AI_KNOWLEDGE_ASSISTANT_RAG**

---
## OVERVIEW

This project is about RAG system.
Build an end-to-end RAG-powered AI Knowledge Assistant that can:
1. Load a document collection.
2. Split documents into meaningful chunks.
3. Generate embeddings.
4. Store chunks in a vector database.
5. Retrieve relevant chunks for user questions.
6. Generate grounded answers using Groq-hosted LLMs.
7. Provide source citations.
8. Refuse or clarify when the answer is not available in the retrieved context.
9. Show retrieved context snippets for transparency.

---
## Requirements
groq>=1.2.0
ipykernel>=7.2.0
python-dotenv>=1.2.2
tiktoken==0.9.0
pypdf==5.4.0
langchain==0.3.20
langchain-community==0.3.19
langchain-chroma==0.2.2
sentence-transformers==5.1.2
chromadb==0.6.3
langchain-cohere==0.4.5

---
## steps

step-1
uv init

step-2
Make a virtual enviroment and activate it

step-3: to make database (1 time process)
```python
python run.py
```

step-4: Run Chatbot
```python
python app.py
```

step-5: To Exit-> type exit in terminal
