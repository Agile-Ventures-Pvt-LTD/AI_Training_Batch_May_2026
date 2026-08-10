# Name

Palak

# Assignment / Project Title

Advanced RAG Optimization using Batch-Level Hypothetical Questions

# Short Description

This project implements an advanced Retrieval-Augmented Generation (RAG) optimization technique using **Hypothetical Question Generation** at the batch level.

Instead of generating hypothetical questions for every individual chunk, document chunks are grouped into batches of 50 chunks. For each batch, an LLM generates three broad hypothetical questions representing the information contained within that batch. These questions are stored in a separate ChromaDB collection and used as an additional retrieval layer.

During retrieval:

1. User queries are matched against the hypothetical-question collection.
2. The most relevant batch is identified.
3. Associated chunk IDs are retrieved from metadata.
4. Original chunks corresponding to those IDs are fetched.
5. Retrieved context is optionally compressed.
6. The final context is passed to the LLM for answer generation.

This hierarchical retrieval approach reduces the number of vectors stored while improving semantic retrieval for complex queries.

# Methodology

## Step 1: Create Original Vector Database

* Tesla 10-K annual reports were chunked.
* Chunks were embedded using NVIDIA embeddings.
* Chunks were stored in ChromaDB.

Collection:

```text
tesla-10k-2019-to-2023
```

---

## Step 2: Batch Formation

Chunks were grouped into batches of 50.

Example:

```text
Batch 0:
Chunk 0
Chunk 1
...
Chunk 49
```

---

## Step 3: Generate Hypothetical Questions

For every batch:

* LLM receives all 50 chunks.
* Generates exactly 3 hypothetical questions representing the information contained in that batch.

Example:

```text
What factors affect Tesla's production and delivery performance?

How does Tesla manage operational and manufacturing risks?

What disclosures help evaluate Tesla's financial and operational health?
```

---

## Step 4: Store Batch-Level Questions

A second collection is created:

```text
tesla-10k-hypothetical-questions-batch
```

Each question stores metadata:

```json
{
  "batch_id": "batch_12",
  "chunk_ids": ["text_600", "text_601", "..."]
}
```

---

## Step 5: Retrieval

When a user submits a query:

```text
User Query
↓
Batch Hypothetical Question Collection
↓
Top Matching Batch
↓
Retrieve Associated Chunk IDs
↓
Fetch Original Chunks
↓
Generate Context
↓
LLM Answer
```

---

## Step 6: Context Compression

Retrieved chunks are combined and compressed using an LLM-based compression stage to keep only information relevant to the query.

Benefits:

* Reduced context size
* Higher signal-to-noise ratio
* Improved answer quality

---

## Step 7: Answer Generation

The compressed context is passed to the Q&A model.

Final output includes:

* User Question
* Retrieved Context
* Generated Answer

# Advantages of Batch-Level Hypothetical Questions

## Traditional Retrieval

```text
User Query
↓
Chunk Embeddings
↓
Top Chunks
```

Problems:

* Vocabulary mismatch
* Semantic gap between query and chunk text
* Missing relevant chunks

---

## Hypothetical Question Retrieval

```text
User Query
↓
Hypothetical Questions
↓
Relevant Batch
↓
Relevant Chunks
```

Advantages:

* Better semantic matching
* Improved recall
* Better handling of abstract queries
* Reduced vector count

# Experimental Setup

## Original Collection

```text
3337 chunks
```

## Batch Size

```text
50 chunks per batch
```

## Number of Batches

```text
67 batches
```

## Hypothetical Questions Generated

```text
67 × 3
=
201 vectors
```

Compared to chunk-level generation:

```text
3337 × 3
=
10011 vectors
```

This significantly reduces storage and retrieval complexity.

# Steps to Run

## Install Dependencies

```bash
pip install chromadb
pip install langchain
pip install langchain-openai
pip install langchain-chroma
pip install openai
pip install groq
pip install sentence-transformers
```

## Set Environment Variables

```bash
NVIDIA_API_KEY=your_key
GROQ_API_KEY=your_key
```

## Run Notebook

Execute notebook cells in order:

1. Create Vector Database
2. Generate Batch Hypothetical Questions
3. Store Questions in ChromaDB
4. Retrieve Relevant Batch
5. Expand Chunk IDs
6. Compress Context
7. Generate Answer
8. Evaluate Results

# Libraries Used

* ChromaDB
* LangChain
* LangChain Chroma
* OpenAI SDK
* NVIDIA NIM APIs
* Groq API
* Sentence Transformers
* Python


# Conclusion

The batch-level hypothetical question approach creates a lightweight hierarchical retrieval system that improves semantic matching while reducing storage requirements from over 10,000 vectors to approximately 200 vectors. This method provides an efficient alternative to chunk-level hypothetical question generation and demonstrates a scalable strategy for improving RAG retrieval quality.
