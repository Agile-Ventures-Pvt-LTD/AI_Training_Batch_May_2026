# Assignment 03 - Hypothetical Question Retrieval (HyDE-style RAG)

## Participant Name
Simran Kaur

## Description

This assignment implements a Hypothetical Question Retrieval pipeline on Tesla 10-K annual reports (2019–2023).

Instead of directly retrieving document chunks, the system first generates hypothetical questions from groups of Tesla 10-K chunks and stores these questions in a separate vector database.

During retrieval:

1. User benchmark questions are embedded.
2. Similar hypothetical questions are retrieved.
3. The parent Tesla chunks associated with those hypothetical questions are identified.
4. Relevant chunk content is assembled as context.
5. An LLM generates the final answer using only the retrieved context.

This approach improves semantic retrieval by matching user intent against generated questions rather than directly against raw document chunks.

---

## Objective

Build a retrieval system that:

- Generates hypothetical questions from Tesla annual report chunks.
- Creates a dedicated hypothetical-question vector database.
- Retrieves relevant hypothetical questions for benchmark queries.
- Maps retrieved questions back to original Tesla chunks.
- Uses retrieved chunk context to generate grounded answers.

---

## Dataset

Tesla 10-K Annual Reports:

- 2019
- 2020
- 2021
- 2022
- 2023

Source collection:

```text
tesla-10k-2019-to-2023
```

Stored inside:

```text
./tesla_db
```

---

## Methodology

### Step 1: Load Tesla Chunks

Load all chunks from the ChromaDB collection.

Each chunk contains:

- Chunk ID
- Chunk Text
- Metadata

---

### Step 2: Chunk Compression

To reduce token usage before sending data to the LLM:

- Split chunk into sentences.
- Apply TF-IDF scoring.
- Select top informative sentences.
- Create a compressed representation.

Benefits:

- Lower token consumption.
- Faster processing.
- Reduced API cost.

---

### Step 3: Noise Filtering

Low-value chunks are ignored.

Examples:

- Table of contents
- Signatures
- Index pages
- Auditor information

---

### Step 4: Hypothetical Question Generation

Chunks are grouped into batches of 100.

For each batch:

- Send compressed chunk content to the LLM.
- Generate exactly 3 hypothetical retrieval questions.

Example:

```text
What risks could affect Tesla's future manufacturing capacity?

How does Tesla manage supply chain and battery sourcing challenges?

What factors influence Tesla's operating cash flow and profitability?
```

Generated questions are saved in:

```text
batch_hypothetical_questions.json
```

---

### Step 5: Build Hypothetical Question Vector Store

Each generated hypothetical question becomes a document.

Metadata stored:

```json
{
  "batch_id": 0,
  "start_chunk": 0,
  "end_chunk": 99,
  "chunk_ids": "text_0,text_1,..."
}
```

Embeddings are generated using:

```text
sentence-transformers/all-mpnet-base-v2
```

Stored in Chroma collection:

```text
tesla_hypothetical_questions
```

---

### Step 6: Retrieval

For every benchmark question:

1. Embed user query.
2. Retrieve top-k hypothetical questions.
3. Extract parent chunk IDs.
4. Fetch original Tesla chunks.
5. Construct retrieval context.

---

### Step 7: Answer Generation

The retrieved chunk content is passed to the LLM.

Prompt instructions:

- Answer only using provided context.
- Do not use external knowledge.
- Return "I don't know" if answer is unavailable.

---

## Benchmark Questions

### HQ1

What should a board member ask about risks that could prevent Tesla from meeting production, delivery, or scaling expectations?

### HQ2

How should an analyst investigate the relationship between product defects, warranty or service obligations, customer trust, and brand risk?

### HQ3

What evidence helps determine whether future cash flow depends more on capital expenditure discipline, working capital, or operating income?

### HQ4

Which disclosures help evaluate technology, cybersecurity, data, or AI operational risk even if the user does not explicitly say cybersecurity?

---

## Project Structure

```text
project/
│
├── tesla_db/
│
├── batch_hypothetical_questions.json
│
├── batch_checkpoint.json
│
├── outputs.json
│
├── assignment_03_solution.ipynb
│
└── README.md
```

---

## How to Run

### 1. Install Dependencies

```bash
pip install chromadb
pip install openai
pip install numpy
pip install scikit-learn
pip install sentence-transformers
pip install langchain
pip install langchain-core
pip install langchain-community
pip install langchain-chroma
```

---

### 2. Set NVIDIA API Key

Linux / Mac:

```bash
export NVIDIA_API_KEY="your_key"
```

Windows:

```cmd
set NVIDIA_API_KEY=your_key
```

---

### 3. Run Notebook

Open:

```text
assignment_03_solution.ipynb
```

Run cells sequentially:

1. Load Tesla chunks
2. Compress chunks
3. Generate hypothetical questions
4. Build hypothetical vector store
5. Retrieve benchmark questions
6. Generate final answers
7. Export outputs

---

## Required Libraries

```text
chromadb
openai
numpy
scikit-learn
sentence-transformers
langchain
langchain-core
langchain-community
langchain-chroma
```

---

## Assumptions

1. Tesla chunk collection already exists inside ChromaDB.

2. Chunk IDs are unique.

3. NVIDIA API access is available.

4. Benchmark evaluation uses only hypothetical retrieval.

5. No baseline retrieval comparison was implemented.

6. Each batch contains approximately 100 Tesla chunks.

7. Exactly 3 hypothetical questions are generated per batch.

---

## Output Files

### 1. batch_hypothetical_questions.json

Contains generated hypothetical questions.

Example:

```json
{
  "batch_id": 0,
  "start_chunk": 0,
  "end_chunk": 99,
  "hypothetical_questions": [
    "...",
    "...",
    "..."
  ]
}
```

---

### 2. outputs.json

Contains final benchmark results.

Example:

```json
{
  "question_id": "HQ1",
  "user_query": "...",
  "retrieved_hypothetical_questions": [],
  "parent_chunks_used": [],
  "final_answer": "...",
  "citations": []
}
```

---

## Retrieval Pipeline Flow

```text
Tesla Chunks
      │
      ▼
Chunk Compression
      │
      ▼
Batch of 100 Chunks
      │
      ▼
Generate 3 Hypothetical Questions
      │
      ▼
Store in ChromaDB
      │
      ▼
User Query
      │
      ▼
Retrieve Similar Hypothetical Questions
      │
      ▼
Extract Parent Chunk IDs
      │
      ▼
Retrieve Original Tesla Chunks
      │
      ▼
Build Context
      │
      ▼
LLM Answer Generation
      │
      ▼
outputs.json
```

---

## Results

The system successfully:

- Generated hypothetical retrieval questions.
- Built a dedicated hypothetical-question vector database.
- Retrieved relevant parent chunks.
- Produced grounded answers for benchmark questions.
- Exported structured outputs in JSON format.

This demonstrates an end-to-end Hypothetical Question Retrieval pipeline for Retrieval-Augmented Generation (RAG) over Tesla 10-K filings.