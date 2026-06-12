# AI Knowledge Assistant

A command-line RAG application for answering questions from local business documents. It loads PDF, TXT, Markdown, and HTML files, creates sentence-transformer embeddings, stores them in Chroma, retrieves relevant chunks, and uses Groq to produce grounded answers with citations.

## Participant Name
Nandani Bisht

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add a Groq API key to `.env`, then place documents in `data/raw/`.

## Build The Index

```powershell
python app.py index --reset
```

The default chunk size is 1,000 characters with 150 characters of overlap. This keeps chunks focused enough for retrieval while retaining context across boundaries. Both values can be changed in `.env` or with command-line options.

## Ask Questions

```powershell
python app.py ask "What are the main business segments?"
python app.py chat
```

Each answer includes its query type, answerability, confidence, sources, and retrieved chunk previews. Questions and answers are appended to `data/logs/query_logs.jsonl`.

## Business Use Case

Business users face the following challenges:
1. Knowledge is spread across long documents.
2. Users do not know where to search.
3. Manual document reading is time-consuming.
4. Answers from normal LLMs may hallucinate.
5. Users need source references before trusting answers.
6. Similar business questions may require comparing multiple document 
sections.
7. Some questions cannot be answered from the available documents and 
should be handled safely.

The proposed system should reduce document search time and improve answer 
reliability by using Retrieval-Augmented Generation.


## Project Structure

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
├── output_parser.py
├── logger.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ ├── raw/
│ ├── processed/
│ └── vector_store/
│
├── logs/
│ └── query_logs.jsonl
│
├── outputs/
│ └── benchmark_results.json
│
└── tests/
 └── test_retrieval.py






 
