# HyDE (Hypothetical Document Embeddings) for Retrieval-Augmented Generation

## Overview

This project demonstrates the implementation of **HyDE (Hypothetical Document Embeddings)** in a Retrieval-Augmented Generation (RAG) pipeline.

HyDE improves retrieval quality by first generating a hypothetical answer/document for a user's query and then using the embedding of that generated document to retrieve relevant information from the vector database.

This technique helps improve retrieval performance for ambiguous, short, or complex user queries.

---

## Objective

Traditional semantic search directly embeds the user query and retrieves similar documents.

HyDE enhances retrieval by:

1. Generating a hypothetical answer to the query.
2. Creating embeddings from the generated answer.
3. Using those embeddings for document retrieval.
4. Passing the retrieved context to the LLM for final response generation.

---

## Workflow

### Step 1: User Query

Example:

```text
What are Tesla's major revenue sources?
```

### Step 2: Generate Hypothetical Answer

The LLM generates a hypothetical response:

```text
Tesla generates revenue primarily through vehicle sales,
energy generation and storage products, regulatory credits,
and related services.
```

### Step 3: Create Embeddings

The hypothetical answer is converted into vector embeddings.

### Step 4: Vector Search

The embedding is used to retrieve relevant chunks from the ChromaDB vector store.

### Step 5: Context Retrieval

Top relevant documents are retrieved and ranked.

### Step 6: Final Answer Generation

Retrieved context is provided to the LLM for generating the final response.

---

## Architecture

```text
User Query
    │
    ▼
Generate Hypothetical Document
    │
    ▼
Create Embedding
    │
    ▼
Vector Database Search
    │
    ▼
Retrieve Relevant Context
    │
    ▼
Generate Final Answer
```

---

## Technologies Used

* Python
* LangChain
* ChromaDB
* Groq API
* Hugging Face Embeddings
* Jupyter Notebook

---

## Project Structure

```text
AG0854__3/
│
├── .gitignore
├── .python-version
├── README.md
├── requirements.txt
├── pyproject.toml
├── main.py
├── Hypothetical_questions.ipynb
│
├── tesla-annual-reports/
│   ├── tsla-10k_20191231-gen_0.pdf
│   ├── tsla-10k_20201231-gen.pdf
│   ├── tsla-10ka_20211231-gen.pdf
│   ├── tsla-20221231-gen.pdf
│   └── tsla-20231231-gen.pdf
│
└── tesla_db/
```

---

## Advantages of HyDE

* Improves retrieval quality.
* Handles ambiguous queries effectively.
* Increases semantic matching capability.
* Enhances context relevance.
* Improves final answer accuracy.

---

## Example

### User Query

```text
How does Tesla earn money?
```

### Hypothetical Document

```text
Tesla earns revenue through electric vehicle sales,
energy storage solutions, solar products, services,
and regulatory credit sales.
```

### Retrieved Documents

Relevant Tesla annual report sections are retrieved using the generated embedding.

### Final Response

The LLM produces a grounded answer using the retrieved context.

---

## Challenges

* Additional LLM call for hypothetical document generation.
* Increased latency compared to standard retrieval.
* Higher token usage.
* Retrieval quality depends on the quality of generated hypothetical documents.

---

## Conclusion

HyDE is a powerful retrieval enhancement technique that improves document recall and retrieval quality in RAG systems. By generating hypothetical documents before retrieval, the system can better understand user intent and retrieve more relevant information, leading to higher-quality responses.

---

## Author

**Divya Khandelwal**

Assignment 03 – HyDE (Hypothetical Document Embeddings) in RAG

AI Training Batch May 2026
