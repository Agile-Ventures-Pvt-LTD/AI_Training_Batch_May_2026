# Production-Grade Marketplace RAG Support Agent

## Overview

It is an AI-powered RAG Ecommerce support system built using Pydantic AI, Guardrail AI, Groq LLM,RAG, and SQLite.

The agent can answer ecommerce queries by retrieving information from knowledge base database through a set of specializes tools as we used in this project.
 
For Testing we use DeepEval Techniques like Answer Relevancy, Contexual Precision

---

## Tech Stack

* Python 3.12+
* LangChain
* Pydantic-AI
* Guardrail-AI
* DeepEval
* Groq API
* SQLite
* python-dotenv
* chroma
* HuggingFace
* RAG


---

## Project Structure

```text
rag-ecommerce-support-chatbot/
│
├── requirements.txt
├── .env.example
├── README.md
│
├── chroma_db/
│   └── chroma.sqlite3
├── data/
│   └── seller_guide.pdf
├── src/
│   └── agent.py
│   └── database.py
│   └── guardrails_config.py
│
├── outputs/
│   ├── evaluation_results.json
```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd rag-ecommerce-support-chatbot
```

### 2. Create Virtual Environment

```bash
uv venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```
GROQ_API_KEY = your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2 
DATA_PATH=data
VECTOR_STORE_PATH=chroma_db
CHUNK_SIZE=800 
CHUNK_OVERLAP=150 
TOP_K=5

```

---

## Running the Application

```bash
python src\agent.py
```
---
## For creating vector db
```bash
python src\database.py
```
---
## For Running Test Case
```bash
python test\test_rag_metrics.py
```

## Available Tools

1. calculate_average_selling_price
2. query_fulfillment_workflows

## Example Queries

```text
1.Can you check my fulfillment rules and calculate Average Selling Price?
2.What is the best recipe for baking chocolate chip cookies?
```

## Output Example
Seller Query: Can you check my fulfillment rules and calculate Average Selling Price?

Status: success
Agent Output:
I’ve reviewed the fulfillment guidelines for you: our policy requires a 24‑hour turnaround on order processing to protect your Detailed Seller Ratings (DSRs) and ensure timely delivery.

Based on the sales data in our system, your current Average Selling Price (ASP) is $42.50 across all channels.

Let me know if you need any further assistance with your fulfillment settings or other performance metrics.

Seller Query: What is the best recipe for baking chocolate chip cookies?
Status: fallback
Agent Output:
I’m sorry, but I can’t help with that.
---


---

<!-- ## Security Features

The agent must review the response for unsafe recommendations.
Safety rules:
1. Do not ask for passwords.
2. Do not ask for OTPs.
3. Do not ask for MFA codes.
4. Do not ask users to disable security controls.
5. Do not recommend storing company data in personal drives.
6. Do not expose sensitive user information unnecessarily. -->

---


## Future Enhancements

* Streamlit UI
* FastAPI deployment
* Advanced Graph Routing & State Analytics
* Enhanced RAG Architecture (Advanced Retrieval)
* Enterprise Integration & Real-time Data Sync

---

## Author
Ashish Sinha
