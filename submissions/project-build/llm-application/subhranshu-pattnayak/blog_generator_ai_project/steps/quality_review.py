from groq_client import call_json_llm

def quality_review(draft: str, guidelines: str, seo_keywords=None, cta: str = "") -> str:
    seo_keywords = seo_keywords or []
    prompt = f"""
    Role: Content reviewer.
    Task: Review the draft for relevance, clarity, structure, tone, SEO usage, hallucination risk, and CTA effectiveness.

    Draft: {draft}
    Guidelines: {guidelines}
    SEO Keywords: {', '.join(seo_keywords)}
    CTA: {cta}

    Output JSON:
    {{
        "scores": {{
            "relevance": 0,
            "clarity": 0,
            "structure": 0,
            "tone_alignment": 0,
            "seo_usage": 0,
            "hallucination_risk": 0,
            "cta_effectiveness": 0
        }},
        "strengths": [],
        "improvement_areas": [],
        "final_quality_summary": ""
    }}

    Rules:
    - Scores must be integers from 1 to 5.
    - For hallucination_risk, a higher score means higher risk.
    - Do not invent facts while reviewing.
    - Return valid JSON only.
    """
    return call_json_llm([{"role": "user", "content": prompt}])
