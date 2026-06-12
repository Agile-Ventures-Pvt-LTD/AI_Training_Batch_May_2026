from groq_client import call_json_llm

def generate_seo_metadata(keywords: list) -> str:
    prompt = f"""
    Role: SEO specialist.
    Task: Generate SEO-friendly titles and meta description.

    Example Input:
    Keywords: AI recruitment, hiring automation

    Example Output:
    {{
        "seo_title": "AI Recruitment: Practical Ways to Improve Hiring Workflows",
        "meta_description": "Learn how AI recruitment tools can help teams screen candidates, reduce repetitive work, and improve hiring consistency.",
        "primary_keyword": "AI recruitment",
        "secondary_keywords": ["hiring automation"],
        "suggested_slug": "ai-recruitment-hiring-workflows",
        "search_intent": "Informational"
    }}

    Output Format:
    {{
        "seo_title": "",
        "meta_description": "",
        "primary_keyword": "",
        "secondary_keywords": [],
        "suggested_slug": "",
        "search_intent": ""
    }}

    Keywords: {', '.join(keywords)}

    Rules:
    - SEO title should be concise.
    - Meta description must be under 160 characters.
    - Keywords should be used naturally.
    - Slug must be lowercase and hyphen-separated.
    - Return valid JSON.
    """
    return call_json_llm([{"role": "user", "content": prompt}])
