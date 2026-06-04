# Hypothetical Question Based RAG Pipeline for Tesla Annual Report

## 1. Name

**Mohammad Zaid**

---

## 2. Assignment Title

**Assignment 03 – Retrieval Augmentation using Hypothetical Questions (HyDE-inspired RAG)**

---

## 3. Short Description

This project implements a Retrieval-Augmented Generation (RAG) pipeline on the Tesla Annual Report using a hypothetical question generation approach.

The objective is to improve retrieval performance for abstract and business-oriented user queries by generating synthetic (hypothetical) questions for every document chunk and indexing them in a separate ChromaDB collection.

### Workflow

#### Offline Phase

1. Load document chunks from the existing ChromaDB collection.
2. Generate 3 hypothetical questions for each chunk using an LLM.
3. Store generated questions in a separate ChromaDB collection.
4. Maintain parent-child mapping between hypothetical questions and original chunks.

#### Online Phase

1. User submits a query.
2. Query is matched against the hypothetical question collection.
3. Relevant hypothetical questions are retrieved.
4. Parent chunk IDs are extracted.
5. Original chunks are fetched from the chunk collection.
6. Retrieved context is provided to the LLM.
7. Final answer is generated using the retrieved context.

---

## 4. Steps to Run the Code

### Step 1: Clone Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### Step 2: Create Virtual Environment

```bash
uv init
uv venv
```

Activate environment:

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / Mac

```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install langchain
pip install langchain-community
pip install langchain-chroma
pip install langchain-huggingface
pip install chromadb
pip install openai
pip install tqdm
```

### Step 4: Configure API Key

Create a `.env` file:

```env
NVIDIA_API_KEY=your_api_key_here
```

or

```env
GROQ_API_KEY=your_api_key_here
```

depending on the model provider being used.

### Step 5: Generate Hypothetical Questions

Run notebook cells responsible for:

* Loading chunks
* Batch hypothetical question generation
* Storing hypothetical questions into ChromaDB

### Step 6: Execute Retrieval Pipeline

Run benchmark evaluation cells to:

* Retrieve hypothetical questions
* Retrieve parent chunks
* Generate final answers
* Export benchmark results

### Step 7: Review Outputs

Generated files:

```text
benchmark_results.json
```

---

## 5. Libraries / Packages Required

### Core Libraries

```text
langchain
langchain-community
langchain-chroma
langchain-huggingface
chromadb
openai
tqdm
json
os
time
```

### Embedding Model

```text
sentence-transformers/all-mpnet-base-v2
```

### Vector Database

```text
ChromaDB
```

### LLM

```text
meta/llama-3.1-8b-instruct (NVIDIA NIM)
```

or

```text
openai/gpt-oss-120b (Groq)
```

---

## 6. Assumptions Made

1. The Tesla Annual Report has already been chunked and stored in ChromaDB.
2. Original chunk IDs follow the format:

```text
text_0
text_1
text_2
...
```

3. Generated hypothetical question IDs follow the format:

```text
hq_text_0_0
hq_text_0_1
hq_text_0_2
...
```

4. Each hypothetical question stores a reference to its source chunk using:

```text
parent_chunk_id
```

5. The same embedding model is used for both:

   * Original chunk collection
   * Hypothetical question collection

6. Three hypothetical questions are generated per chunk.

7. Retrieval is performed against the hypothetical question collection first and then mapped back to original chunks.

---

## 7. Output Explanation

### Generated Hypothetical Question Collection

Example:

```json
{
    "hq_id": "hq_text_15_0",
    "parent_chunk_id": "text_15",
    "question": "What risks could affect Tesla's production targets?"
}
```

### Retrieval Flow

```text
User Query
    ↓
Hypothetical Question Collection
    ↓
Parent Chunk IDs
    ↓
Original Chunk Collection
    ↓
LLM
    ↓
Final Answer
```

### Benchmark Output

The benchmark evaluation generates results in the following schema:

```json
{
  "question_id": "HQ1",
  "user_query": "...",
  "retrieved_hypothetical_questions": [],
  "parent_chunks_used": [],
  "final_answer": "...",
  "citations": [],
  "comparison_with_baseline": ""
}
```

### Benchmark Questions

* HQ1: Production, delivery, and scaling risks
* HQ2: Product defects, warranty obligations, and brand risk
* HQ3: Cash flow drivers and financial discipline
* HQ4: Technology, cybersecurity, data, and AI operational risk

### Output Files

```text
generated_hqs.json
benchmark_results.json
```

### Screenshots

Add screenshots of:

1. ChromaDB collections
2. Hypothetical question generation output
3. Retrieval results
4. Benchmark evaluation results
5. Final generated answers

```
```
