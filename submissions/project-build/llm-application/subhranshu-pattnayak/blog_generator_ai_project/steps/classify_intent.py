from groq_client import call_json_llm

def classify_intent(validated_inputs: dict) -> str:
    prompt = f"""
    Role: You are a Senior B2B content strategist.
    Task: Analyze the user-provided blog request and classify the blog intent.

    
    Possible intent categories:
        -THOUGHT_LEADERSHIP
        -PRODUCT_EDUCATION
        -SEO_INFORMATIONAL
        -LEAD_GENERATION
        -COMPARISON
        -ANNOUNCEMENT
        -HOW_TO_GUIDE
    
    Output Format:
    {{
        "blog_intent": "LEAD_GENERATION",
        "target_reader_maturity": "BEGINNER | INTERMEDIATE | ADVANCED",
        "recommended_content_angle": "",
        "reasoning_summary": ""
    }}
    
    Example Input:
    {{
        "blog_topic": "AI in HR",
        "target_audience": "HR leaders",
        "product_or_service_context": "AI tool for recruitment"
    }}

    Example Output:
    {{
        "blog_intent": "PRODUCT_EDUCATION",
        "target_reader_maturity": "Intermediate",
        "recommended_content_angle": "Practical use cases",
        "reasoning_summary": "HR leaders need practical examples of AI in recruitment."
    }}

    Now classify this input:
    {validated_inputs}

    Rules:
    - Do not invent information.
    - Base your answer only on the provided input.
    - If information is missing, mention it.
    - Think through the classification carefully, but return only a concise reasoning summary.
    - Return valid JSON only.
    """
    return call_json_llm([{"role": "user", "content": prompt}])
