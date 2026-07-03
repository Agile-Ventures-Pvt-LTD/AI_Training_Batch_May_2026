# Production-Grade Marketplace RAG Support Agent

## 1. Business Objective & Background
Modern e-commerce marketplaces require highly available, accurate, and secure automated
support for their seller ecosystems. The goal of this project is to build an enterprise-grade,
production-ready Retrieval-Augmented Generation (RAG) chatbot for ShopSphere
Marketplace, a platform hosting thousands of independent business sellers.
The chatbot must accurately ingest complex corporate guidelines—specifically focusing on
advanced business operations, fulfillment strategies, seller ratings, and profitability matrices. It
must answer seller queries instantly while maintaining absolute deterministic safety standards,
ensuring no toxic, profane, or hallucinated outputs are surfaced to end-users

## Run Project

python -m src.app

## requirements

groq
langchain>=0.3.0
langchain-core>=0.3.0
langchain-community>=0.3.0
chromadb>=0.5.0
langchain-chroma>=0.2.0
sentence-transformers>=3.0.0
langchain-huggingface>=0.1.0
pypdf>=5.0.0
unstructured>=0.16.0
python-dotenv>=1.0.1
pydantic>=2.9.0
numpy>=1.26.0
pandas>=2.2.0
tqdm>=4.66.0
rich>=13.9.0
pydantic-ai
pydantic-ai-slim[groq]
guardrails-ai>=0.6.7