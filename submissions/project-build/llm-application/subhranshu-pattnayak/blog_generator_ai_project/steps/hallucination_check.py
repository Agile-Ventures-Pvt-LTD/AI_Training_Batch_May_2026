from groq_client import call_json_llm

def hallucination_check(draft: str, avoid_claims: list, source_context: dict = None) -> str:
    source_context = source_context or {}
    prompt = f"""
    Role: Fact-checker.
    Task: Identify statements in the blog that may require verification or editing.

    Draft: {draft}
    Source Context Provided By User: {source_context}
    Avoid Claims: {', '.join(avoid_claims)}

    Rules:
    - Use only the provided source context as the ground truth.
    - Flag numerical claims, market leadership claims, guaranteed outcomes, legal or compliance claims, customer success claims, competitor claims, certifications, and awards.
    - Flag unsupported claims.
    - Do not invent facts.
    - Return valid JSON.

    Output JSON:
    {{
        "claims_requiring_verification": [],
        "unsupported_claims": [],
        "safe_claims": [],
        "recommended_edits": []
    }}
    """
    return call_json_llm([{"role": "user", "content": prompt}])
