from groq_client import call_json_llm

def suggest_improvements(draft: str) -> str:
    prompt = f"""
    Role: Senior editor.
    Task: Suggest improvements to strengthen the draft.

    Example Suggestions:
    - Add more data points.
    - Shorten long sentences.
    - Clarify technical jargon.

    Draft: {draft}

    Output JSON:
    {{
        "suggestions": []
    }}

    Rules:
    - Focus on practical editorial improvements.
    - Do not ask for fake data, fake customers, or unsupported claims.
    - Return valid JSON only.
    """
    return call_json_llm([{"role": "user", "content": prompt}])
