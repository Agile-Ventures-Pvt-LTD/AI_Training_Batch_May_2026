from groq_client import call_json_llm

def generate_outline(summary: str, audience: str) -> str:
    prompt = f"""
    Role: You are a Blog strategist.
    Task: Create a structured outline for the blog from the given summary for the mentioned audience.
    Summary: {summary}
    Audience: {audience}
    
    Output Format:
    {{
        "title": "",
        "outline": [
            {{
                "section_heading": "",
                "section_purpose": "",
                "key_points_to_cover": []
            }}
        ],
        "cta_placement": "",
        "estimated_word_count": 0
    }}
    
    Example Outline:
    {{
        "sections": [
            "Introduction: Why AI matters in HR",
            "Challenge: Increasing recruitment workload",
            "Solution: AI-powered screening",
            "Benefits: Speed, consistency, fairness",
            "Conclusion: Human + AI collaboration"
        ]
    }}
    
    Rules:
    - Provide clear sections (Intro, Body, Conclusion).
    - Include 4 to 6 main body sections.
    - Include the suggested conclusion and CTA placement.
    - Do not invent facts, statistics, customers, awards, guarantees, or certifications.
    - Return valid JSON.
    """
    return call_json_llm([{"role": "user", "content": prompt}])
