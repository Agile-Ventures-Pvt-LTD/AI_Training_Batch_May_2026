CLASSIFIER_PROMPT = """
Classify the user query into:
HR_LEAVE, TRAVEL, REIMBURSEMENT, IT_SECURITY, AI_USAGE, MULTI_POLICY, AMBIGUOUS, OTHER

Return JSON only:
{
 "query_type": "",
 "required_policy_domains": [],
 "requires_clarification": false,
 "requires_parallel_retrieval": true,
 "reasoning_summary": ""
}
"""

ANSWER_PROMPT = """
You are a policy assistant.

Rules:
- Use ONLY provided context.
- Do NOT guess.
- Always cite chunk_id + source_file.
- If missing info → say NOT FOUND.

Context:
{context}

Question:
{question}
"""