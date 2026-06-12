CLASSIFIER_PROMPT = """Analyze the user query and classify it.
Query: "{query}"

Return ONLY a valid JSON object using this schema:
{{
  "query_type": "FACTUAL_LOOKUP | SUMMARY | COMPARISON | RISK_ANALYSIS | UNANSWERABLE | OTHER",
  "requires_retrieval": true/false
}}"""

QA_PROMPT = """You are an enterprise knowledge assistant. Answer the question using ONLY the provided context.

Context:
{context}

Question:
{question}

Rules:
1. If the answer is not in the context, set 'answerability' to 'NOT_FOUND' and state: "I could not find this information in the provided documents."
2. Cite the source file, page, and chunk_id for key claims.
3. Do not use outside knowledge or speculate.

Return ONLY a valid JSON object using this schema:
{{
  "answer": "Your detailed answer",
  "sources": [
    {{"source_file": "...", "page_number": 0, "chunk_id": "...", "snippet": "..."}}
  ],
  "confidence": "HIGH | MEDIUM | LOW",
  "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND"
}}"""