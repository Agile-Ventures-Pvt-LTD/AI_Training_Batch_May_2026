# RAG Query Expansion Assignment

## 1. Name

**Aditya Sodani**

---

## 2. Assignment Title

**Retrieval-Augmented Generation (RAG) with Query Expansion for Financial Document Analysis**

---

## 3. Short Description

This project implements a Retrieval-Augmented Generation (RAG) system over Tesla Annual Reports and evaluates the impact of Query Expansion on retrieval quality.

The system:

* Loads and processes Tesla 10-K annual reports.
* Splits documents into semantic chunks.
* Creates embeddings using Sentence Transformers.
* Stores embeddings in ChromaDB vector database.
* Generates multiple semantically similar query variations using an LLM.
* Performs retrieval using both:

  * Baseline Retrieval
  * Query Expansion Retrieval
* Compares retrieval coverage between the two approaches.
* Generates grounded answers using retrieved context.
* Stores results, citations, retrieved chunks, and retrieval analysis in JSON format.

The objective is to improve document retrieval performance by expanding user queries and retrieving more relevant context before answer generation.

---

## 4. Steps to Run the Code

### Step 1: Create a Virtual Environment

```bash
uv venv
```

Activate the environment:

```bash
.venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
uv pip install -r requirements.txt
```

### Step 3: Configure API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### Step 4: Prepare Dataset

Place Tesla Annual Report PDF files inside the project folder.

Example:

```text
data/
├── tsla-20211231-gen.pdf
├── tsla-20221231-gen.pdf
├── tsla-20231231-gen.pdf
```

### Step 5: Launch Jupyter Notebook

```bash
jupyter notebook
```

Open:

```text
RAG_query_expansion.ipynb
```

### Step 6: Execute Notebook Cells

Run all cells sequentially:

1. Environment Setup
2. PDF Loading
3. Text Chunking
4. Embedding Generation
5. ChromaDB Vector Store Creation
6. Retriever Setup
7. Query Expansion Generation
8. Baseline Retrieval
9. Expanded Query Retrieval
10. Answer Generation
11. Result Export

---

## 5. Libraries / Packages Required

```text
groq
openai
python-dotenv
langchain
langchain-community
langchain-chroma
chromadb
sentence-transformers
datasets
tiktoken
pypdf
ipykernel
```

Install all dependencies:

```bash
uv pip install -r requirements.txt
```

---

## 6. Assumptions Made

* Tesla annual report PDFs are available locally.
* A valid Groq API key is available.
* Documents contain machine-readable text.
* Internet connectivity is available.
* ChromaDB is used for vector storage.
* Query Expansion improves retrieval by generating semantically related search queries.
* Retrieved chunks contain sufficient context for answer generation.

---

## 7. Output Explanation

### Example Input Query

```text
Does Tesla's growth story appear more constrained by external supply risk or internal execution and cost structure?
```

### Query Expansion Example

Original Query:

```text
Does Tesla's growth story appear more constrained by external supply risk or internal execution and cost structure?
```

Expanded Queries:

```text
Is Tesla's growth story limited more by external supply risks or internal execution and cost structure?

Does the evidence in Tesla's Risk Factors and MD&A suggest that external supply risk or internal execution and cost structure is the bigger constraint on its growth story?

Which factor appears to more restrict Tesla's growth according to the Risk Factors and MD&A disclosures?
```

### System Workflow

1. User submits a query.
2. LLM generates multiple query variations.
3. Baseline retrieval is performed.
4. Expanded-query retrieval is performed.
5. Retrieved chunks are combined and deduplicated.
6. Context is passed to the LLM.
7. Final answer is generated.
8. Retrieval comparison results are stored in JSON format.

### Example Output Structure

```json
{
  "question_id": "Q1",
  "original_query": "...",
  "expanded_queries": [...],
  "baseline_top_chunks": [...],
  "expanded_top_chunks": [...],
  "final_answer": "...",
  "citations": [...],
  "retrieval_improvement_analysis": "Query expansion improved retrieval coverage compared to baseline retrieval."
}
```

---

## Project Outcome

This assignment demonstrates:

* Retrieval-Augmented Generation (RAG)
* Query Expansion Techniques
* Semantic Search
* Financial Document Question Answering
* ChromaDB Vector Database
* Sentence Transformer Embeddings
* Retrieval Evaluation
* Citation-Based Answer Generation
* LangChain RAG Pipelines
* Groq LLM Integration
* JSON Result Export
