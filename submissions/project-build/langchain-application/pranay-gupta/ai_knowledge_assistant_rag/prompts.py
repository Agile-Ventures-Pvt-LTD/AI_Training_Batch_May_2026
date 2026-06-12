from langchain_core.prompts import (
    ChatPromptTemplate
)

QUERY_CLASSIFICATION_PROMPT = (ChatPromptTemplate.from_template(
        """
You are a query classifier.

Classify the user question.

Allowed Types:

FACTUAL_LOOKUP
SUMMARY
COMPARISON
RISK_ANALYSIS
UNANSWERABLE_OR_SPECULATIVE
FOLLOW_UP
OTHER

Return ONLY valid JSON.

Question:
{question}

Output Format:

{{
    "query_type":"",
    "requires_retrieval":true,
    "requires_comparison":false,
    "answer_style":"",
    "reasoning_summary":""
}}
"""
    )
)

RAG_PROMPT = (ChatPromptTemplate.from_template(
        """
You are an enterprise knowledge assistant.

Answer ONLY using the provided context.

Rules:

1. Never use outside knowledge.

2. Never invent facts.

3. Never speculate.

4. If answer not found, say:

"I could not find this in the provided documents."

5. Every important statement must be
supported by retrieved context.

6. Cite source file and page number.

Question:
{question}

Retrieved Context:
{context}

Return ONLY JSON.

{{
    "answer":"",
    "supporting_evidence":[],
    "sources":[],
    "confidence":"",
    "answerability":""
}}
"""
    )
)