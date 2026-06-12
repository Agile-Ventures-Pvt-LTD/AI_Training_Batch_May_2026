# AI Knowledge Assistant for Enterprise Document Question Answering

This is a RAG application built using Python, LangChain, Groq, and ChromaDB.

## Name
Taniya Gupta

## Features
- **Document Loading** 
- **Preprocessing & Chunking** 
- **Vector Search** 
- **Query Classification** 
- **Grounded Answers** 
- **Source Citations** 
- **Query Logging** 

## Setup Instructions

### 1. Prerequisites
- Python 3.11
- Groq API Key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file (copy from `.env.example`) and add your Groq API Key:
```
GROQ_API_KEY=your_groq_key_here
```

### 4. Add Documents
Place your PDF, TXT or MD files in the `data/raw/` directory.

### 5. Run the Application

#### Index your documents:
```bash
python app.py --index
```

#### Ask a question:
```bash
python app.py --query "What are the major risks mentioned?"
```

#### Run benchmarks:
```bash
python app.py --benchmark
```
#### Or run using:
```bash
python app.py
```

## Folder Structure

```text
ai_knowledge_assistant_rag/
│
├── app.py
├── config.py
├── loaders.py
├── chunking.py
├── embeddings.py
├── vector_store.py
├── retriever.py
├── prompts.py
├── chains.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ ├── raw/
│ └── vector_store/
│
├── logs/
│ └── query_logs.jsonl
│
└── outputs/
 └── benchmark_results.json
```

## Benchmark Questions
You can test the assistant with questions like:
1. What are main business segments described in the filings?
2. What risks are mentioned?
3. Summarize the key risk factors in 5 bullet points.
4. What does the document say about automotive revenue or energy generation and storage?
5. Compare the cumulative total return on the common stock with the cumulative total return of the NYSE Technology Index
6. What legal or regulatory risks are mentioned?
7. What will the stock price be?
8. Did the document say that it guarantees future profitability from AI products?

