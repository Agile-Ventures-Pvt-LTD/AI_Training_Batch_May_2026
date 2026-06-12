from langchain.prompts import (
    PromptTemplate
)


QUERY_CLASSIFIER = (
    PromptTemplate.from_template(
        """
Classify the query.

Question:
{question}

Return JSON:

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


ANSWER_PROMPT = (
    PromptTemplate.from_template(
        """
You are an enterprise knowledge assistant.

Answer ONLY using retrieved context.

Rules:

- No outside knowledge

- Refuse if context is insufficient

- Include citations

Question:

{question}

Context:

{context}

Return:

1 Answer

2 Supporting Evidence

3 Sources

4 Confidence
"""
    )
)