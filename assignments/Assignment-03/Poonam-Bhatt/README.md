# Hypothetical Question Generation for Retrieval Improvement in RAG Systems

## 1. Name

Poonam Bhatt

## 2. Assignment / Project Title

Hypothetical Question Generation for Improving Retrieval in RAG Systems

## 3. Short Description of What I Built

This project implements the **Hypothetical Question Generation retrieval enhancement technique** for a Retrieval-Augmented Generation (RAG) system using Tesla Annual Report documents.

The system generates hypothetical retrieval questions for batches of document chunks using **NVIDIA API (Llama-3.1-8B-Instruct model)**.

Workflow:

* Tesla annual report chunks are loaded from ChromaDB.
* Chunks are processed in batches.
* For each batch, the model generates **3 hypothetical retrieval questions**.
* Generated questions are stored inside a JSON file.
* During inference, hypothetical retrieval logic improves semantic matching between user questions and document context.
* Retrieved chunks are passed to the LLM for final answer generation.

## 4. Steps to Run the Code

1. Create virtual environment:

```bash
python -m venv .venv
```

2. Activate environment:

Windows:

```bash
.venv\Scripts\activate
```

3. Install required libraries:

```bash
pip install -r requirements.txt
```

4. Configure NVIDIA API key.

5. Load vector database.

6. Run notebook cells to generate hypothetical questions.

7. Execute retrieval pipeline.

## 5. Libraries or Packages Required

* openai
* chromadb
* langchain
* langchain-community
* langchain-chroma
* json
* os
* time

## 6. Assumptions Made

* Tesla Annual Report chunks are already embedded and stored in ChromaDB.
* NVIDIA API credentials are valid.
* Batch processing is used to reduce rate-limit issues.
* Hypothetical questions improve semantic retrieval quality.

## 7. Output Explanation

Example Batch Output:

```text
Q1
What financial information is discussed in this section?

Q2
What revenue-related details are reported in the batch?

Q3
Which automotive business metrics are described?
```

Stored JSON Example:

```json
{
  "batch_start":0,
  "hypothetical_questions":"Q1 ... Q2 ... Q3 ..."
}
```

Example Final User Query:

```text
What was the automotive revenue in 2021?
```

Example Final Response:

```text
The automotive revenue in 2021 was $47,232 million.
```
