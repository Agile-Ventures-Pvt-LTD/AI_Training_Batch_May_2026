# Retrieval-Augmented Generation (RAG) for Tesla Annual Reports

A production-style Retrieval-Augmented Generation (RAG) system built on Tesla Annual Reports (2019–2023) using ChromaDB, Sentence Transformers, NVIDIA-hosted Llama 3.1 70B, and Advanced Retrieval Techniques such as Hypothetical Question Indexing.

---

## 📌 Project Overview

Large Language Models (LLMs) possess extensive general knowledge but often struggle with domain-specific information and may generate hallucinated responses.

Retrieval-Augmented Generation (RAG) addresses this challenge by retrieving relevant information from an external knowledge base and supplying it as context to the LLM before generating an answer.

This project demonstrates how RAG can be used to analyze Tesla's annual reports and answer natural language questions grounded in real financial documents.

### Key Objectives

- Build an end-to-end RAG pipeline
- Create a searchable knowledge base from Tesla Annual Reports
- Improve retrieval quality using Hypothetical Question Indexing
- Generate grounded responses using Llama 3.1 70B
- Explore advanced retrieval strategies beyond basic semantic search

---

## 🎯 Business Problem

Financial reports contain hundreds of pages of information.

Traditional keyword search systems often fail because users ask questions differently than information is written in the reports.

For example:

**User Query**

> How did Tesla's automotive revenue perform in 2022?

**Document Text**

> Revenue generated from automotive sales increased significantly during fiscal year 2022.

Although both statements refer to the same concept, keyword search may miss the connection.

This project solves the problem through semantic retrieval and LLM-powered reasoning.

---

# 🏗️ System Architecture

## Baseline RAG Pipeline

```text
User Query
    │
    ▼
Embedding Model
    │
    ▼
Vector Search (ChromaDB)
    │
    ▼
Top-K Relevant Chunks
    │
    ▼
Prompt Construction
    │
    ▼
Llama 3.1 70B
    │
    ▼
Generated Response
```

---

## Advanced RAG Pipeline

The advanced version introduces Hypothetical Question Indexing.

```text
Documents
    │
    ▼
Chunking
    │
    ▼
Generate Hypothetical Questions
    │
    ▼
Create Embeddings
    │
    ▼
Store in ChromaDB

--------------------------------

User Query
    │
    ▼
Similarity Search
    │
    ▼
Relevant Hypothetical Questions
    │
    ▼
Associated Document Chunks
    │
    ▼
Llama 3.1 70B
    │
    ▼
Final Answer
```

---

# 📂 Dataset

The knowledge base consists of Tesla Annual Reports (Form 10-K) from:

- 2019
- 2020
- 2021
- 2022
- 2023

These reports include:

- Financial Statements
- Revenue Information
- Automotive Segment Performance
- Energy Generation & Storage
- Risk Factors
- Business Strategy
- Corporate Governance
- Operational Metrics

### Data Source

Tesla Investor Relations

https://ir.tesla.com

---

# ⚙️ Technologies Used

| Component | Technology |
|------------|------------|
| LLM | Llama 3.1 70B |
| API Provider | NVIDIA AI Endpoints |
| Vector Database | ChromaDB |
| Framework | LangChain |
| Embedding Model | Sentence Transformers |
| Document Loader | PyPDFLoader |
| Programming Language | Python |
| Notebook Environment | Jupyter Notebook |

---

# 🧠 Embedding Model

The project uses:

```python
sentence-transformers/all-MiniLM-L6-v2
```

Advantages:

- Fast inference
- Lightweight
- Strong semantic understanding
- Suitable for retrieval tasks

The model converts both documents and user queries into dense vector representations.

---

# 🔍 Baseline RAG Implementation

## Step 1: Document Loading

Tesla annual reports are loaded using:

```python
PyPDFLoader
```

---

## Step 2: Text Chunking

Documents are split into smaller chunks to improve retrieval granularity.

Benefits:

- Better semantic matching
- Reduced context size
- Faster retrieval

---

## Step 3: Embedding Generation

Each chunk is converted into a vector embedding.

Example:

```python
embedding = model.encode(chunk)
```

---

## Step 4: Vector Database Creation

Embeddings are stored in ChromaDB.

```python
Chroma
```

This enables efficient similarity search.

---

## Step 5: Retrieval

For each user query:

1. Generate query embedding
2. Perform similarity search
3. Retrieve top-k relevant chunks

---

## Step 6: Response Generation

Retrieved context is inserted into a prompt and sent to:

```text
Llama 3.1 70B
```

The model generates a grounded answer using the retrieved evidence.

---

# 🚀 Advanced Retrieval: Hypothetical Question Indexing

## Motivation

Traditional semantic search retrieves documents directly.

However, users rarely phrase questions exactly as information appears in documents.

Example:

### User Query

> What challenges did Tesla face in battery manufacturing?

### Document Text

> Battery production constraints affected operational efficiency.

Although semantically related, retrieval quality may degrade.

---

## Solution

Generate synthetic questions for every document chunk.

Example:

### Original Chunk

```text
Battery production constraints affected operational efficiency.
```

### Generated Questions

```text
What manufacturing challenges did Tesla face?

What impacted battery production efficiency?

What operational issues were caused by battery constraints?
```

These questions are embedded and indexed.

---

## Benefits

- Improved recall
- Better semantic matching
- More robust retrieval
- Enhanced user experience

---

# 📊 Project Workflow

## Baseline System

```text
PDF Reports
    │
    ▼
Chunking
    │
    ▼
Embeddings
    │
    ▼
ChromaDB
    │
    ▼
Retriever
    │
    ▼
LLM
```

---

## Enhanced System

```text
PDF Reports
    │
    ▼
Chunking
    │
    ▼
Generate Questions
    │
    ▼
Embeddings
    │
    ▼
ChromaDB
    │
    ▼
Retriever
    │
    ▼
LLM
```

---

# 📈 Evaluation

The project compares:

### Baseline Retrieval

- Document chunk embeddings only

### Advanced Retrieval

- Hypothetical question embeddings

Evaluation focuses on:

- Retrieval relevance
- Semantic recall
- Response quality
- Context coverage

---

# 💡 Example Queries

```text
What was Tesla's automotive revenue in 2022?

What risks were highlighted in the 2023 annual report?

How did Tesla's energy generation business perform?

What factors affected Tesla's profitability?

What challenges were discussed regarding battery production?
```

---

# 📁 Repository Structure

```text
.
├── data/
│   ├── Tesla_2019.pdf
│   ├── Tesla_2020.pdf
│   ├── Tesla_2021.pdf
│   ├── Tesla_2022.pdf
│   └── Tesla_2023.pdf
│
├── chroma_db/
│
├── notebooks/
│   └── RAG_TESLAReports.ipynb
│
├── README.md
│
└── requirements.txt
```

---

# 🔧 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/tesla-rag.git

cd tesla-rag
```

---

## Create Virtual Environment

```bash
python -m venv venv

source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Open:

```text
RAG_TESLAReports.ipynb
```

Execute cells sequentially.

---

# 🔮 Future Improvements

Potential enhancements include:

### Hybrid Search

Combine:

- BM25
- Dense Retrieval

---

### Re-ranking

Use:

- Cross Encoders
- Cohere Rerank
- BGE Reranker

---

### Parent-Child Retrieval

Improve context aggregation.

---

### Metadata Filtering

Filter results by:

- Year
- Section
- Topic

---

### Automated Evaluation

Implement:

- RAGAS
- TruLens
- DeepEval

---

### Citation-Based Responses

Provide page references alongside generated answers.

---

# 📚 Key Learnings

This project demonstrates:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Embedding Models
- Prompt Engineering
- Financial Document Analysis
- Advanced Retrieval Techniques
- LLM Grounding Strategies

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Feel free to open an issue or submit a pull request.

---

# 📜 License

This project is licensed under the MIT License.

---

# ⭐ Acknowledgements

- Tesla Investor Relations
- LangChain
- ChromaDB
- NVIDIA AI Endpoints
- Sentence Transformers
- Meta Llama Team

---

If you found this project useful, consider giving the repository a ⭐.