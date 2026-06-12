from groq_client import call_json_llm

def generate_linkedin_post(topic: str, cta: str) -> str:
    prompt = f"""
    Role: Social media strategist.
    Task: Write a LinkedIn post promoting the blog.

    Example Input:
    Topic: AI in recruitment
    CTA: Download the hiring workflow checklist.

    Example Output:
    {{
        "linkedin_post": "Hiring teams are under pressure to move faster without losing quality. AI can help by reducing repetitive screening work, summarizing candidate information, and keeping recruiters focused on human judgment. Download the checklist to see where AI can support your hiring workflow.",
        "hashtags": ["#AIRecruitment", "#Hiring", "#HRTech"]
    }}

    Topic: {topic}
    CTA: {cta}

    Output JSON:
    {{
        "linkedin_post": "",
        "hashtags": []
    }}

    Rules:
    - Include a hook, short explanation, business relevance, and call to action.
    - Include 3 to 5 relevant hashtags.
    - Keep it concise and professional.
    - Return valid JSON only.
    """
    return call_json_llm([{"role": "user", "content": prompt}])
