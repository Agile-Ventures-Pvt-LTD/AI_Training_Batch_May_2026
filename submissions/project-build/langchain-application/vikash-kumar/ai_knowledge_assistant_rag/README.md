# Project Build 3: AI Knowledge Assitant

A business team has a large set of internal knowledge documents such as annual 
reports, policies, product documentation, operating procedures, and compliance 
documents. Employees often spend significant time searching through these 
documents to find accurate answers.

The company wants to build an AI Knowledge Assistant that can answer user 
questions using only the provided document collection.
The assistant must retrieve relevant document chunks, pass them as context to an 
LLM, generate a grounded answer, and show source references so the user can 
verify the response.

The application should behave like a realistic enterprise knowledge assistant, not a 
simple chatbot. It must support document ingestion, chunking, embeddings, 
vector storage, retrieval, prompt-based answer generation, source citations, 
fallback behavior, and basic evaluation

# Document Embedded (Datasets)

Tesla SEC Filings / Annual Reports
https://s2.q4cdn.com/299287126/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf 

# Approach

We need to Load Document collection from the pdf and then split into the chunks, generate embeddings, store chunks in vector database, retrieve relevant chunks , Generate Grounded Answers, Source Citations, Refuse or clarify when answer is not available, Show retreived context snippets, Save User Queries. Basically, we are utilizing the RAG system to achieve the solution of the business problem.

# FRs

1. Document Upload/ Loading
2. Document Preprocessing
3. Document Chunking
4. Embedding Generation
5. Vector Store Creation
6. Retriever Implementation
7. Query Type Classification
8. RAG Prompt Template
9. Answer Generation
10. Source Citation Display
11. Retrieved Context Debug View
12. Answerability and Hallucination Control
13. Query Logging
14. Basic Evaluation Set


# NFRs

1. Usability
2. Maintainability
3. Reliability
4. Security
5. Performance

# Target Users
1. Bussiness Analyst / Operations User
2. Manager / Decision Maker
3. Compliance / Risk Reviewer
