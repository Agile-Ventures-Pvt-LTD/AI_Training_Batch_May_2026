# AI Knowledge Assistant (RAG)

Lightweight Retrieval-Augmented Generation (RAG) assistant built with LangChain. This project demonstrates how to ingest documents, create embeddings, store them in a vector store, and answer user queries by combining retrieved context with a language model.

## Features

- Document ingestion and preprocessing (PDF, TXT, Markdown)
- Embeddings generation using supported embedding models
- Vector store for fast semantic retrieval
- Prompting pipeline that combines retrieved context with LLM responses
- Minimal example scripts for indexing and querying

## Directory layout

- data/                -- documents to index
- type_loader          -- different types of individual loaders
- loaders.py           -- multitype document loader
- logger.py            -- logs interaction
- retriever.py         -- retrieves relevant docs from vector db
- embeddings.py        -- provides embedding object
- vector-store         -- to add chunks
- chunking.py          -- creates chunks out of loaded documents
- config.py            -- configures environment
- prompts.py           -- stores all prompts
- README.md            -- this file

## Requirements

- Python 3.8+
- pip
- A supported LLM and embedding provider (OpenAI, local LLMs, etc.)

Install dependencies:

pip install -r requirements.txt
or
uv sync

## Configuration

Create a .env file or export environment variables for your provider keys, for example:

GROQ_API_KEY=your_api_key

## Quick start

1. Run query:

	uv run app.py