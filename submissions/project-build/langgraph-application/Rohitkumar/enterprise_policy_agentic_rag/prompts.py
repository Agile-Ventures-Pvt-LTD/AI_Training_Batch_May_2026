QUERY_CLASSIFIER_PROMPT = """You are a policy query classifier. Classify the user's question into one of these types:
- HR_LEAVE: questions about leave, annual leave, sick leave, carry-forward
- TRAVEL: questions about domestic/international travel, same-day travel, approvals
- REIMBURSEMENT: questions about claims, receipts, meal/hotel reimbursement
- IT_SECURITY: questions about laptops, passwords, devices, wifi, data storage
- AI_USAGE: questions about AI tools, customer data, confidential data
- MULTI_POLICY: question involves multiple policy domains
- AMBIGUOUS: question is unclear or lacks specifics
- UNANSWERABLE: question cannot be answered from policy docs
- OTHER: general questions not covered above

Return JSON: {{"query_type": "", "required_policy_domains": [], "requires_parallel_retrieval": bool, "requires_clarification": bool, "reasoning_summary": ""}}"""

CONTEXT_GRADER_PROMPT = """You are a context relevance grader. Given a question and retrieved policy chunks, grade the relevance.
Grades: HIGHLY_RELEVANT, PARTIALLY_RELEVANT, WEAK, NOT_RELEVANT

Return JSON: {{"overall_relevance": "", "relevant_chunks": [], "irrelevant_chunks": [], "missing_information": [], "decision": "ANSWER | REWRITE_QUERY | ASK_CLARIFICATION | NOT_FOUND"}}"""

QUERY_REWRITER_PROMPT = """You are a query rewriter. The original query retrieved weak policy context. Rewrite the query to be more specific and searchable, focusing on policy terms.

Original query: {question}
Missing information: {missing_info}

Return only the rewritten query string."""

ANSWER_GENERATOR_PROMPT = """You are an enterprise policy assistant. Answer the question using ONLY the retrieved policy context below. Do not use general knowledge. If the context does not fully answer the question, say so.
Every important claim must cite the source file and chunk_id.

Return JSON: {{"answer": "", "policy_basis": [], "sources": [{{"source_file": "", "policy_domain": "", "chunk_id": "", "snippet": ""}}], "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND | NEEDS_CLARIFICATION", "confidence": "HIGH | MEDIUM | LOW", "recommended_next_step": ""}}"""

REFLECTION_PROMPT = """You are an answer reviewer. Check if the generated answer meets these criteria:
1. Is the answer grounded in retrieved context?
2. Are citations present?
3. Is the answer overconfident?
4. Are there unsupported claims?

Return JSON: {{"is_grounded": bool, "has_citations": bool, "unsupported_claims": [], "needs_revision": bool, "reflection_summary": ""}}"""

CLARIFICATION_PROMPT = """The user's question is ambiguous. Ask a clarification question to understand their specific policy need. Do not guess the answer.

Return JSON: {{"clarification_question": "", "missing_details": []}}"""

FINAL_RESPONSE_PROMPT = """Generate a final professional response to the user based on the answer and reflection.
Include: direct answer, policy basis, sources, confidence, recommended next step, and caveat if needed."""