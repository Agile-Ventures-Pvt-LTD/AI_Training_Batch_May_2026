from groq_client import call_json_llm

def summarize_notes(context: str, key_points: list) -> str:
    prompt = f"""
    Role: You are a Content analyst.
    Task: Summarize the provided product context and key points into a concise brief.
    
    Bad Example:
    "This product is amazing and will revolutionize everything."  # Too vague, hype

    Good Example:
    "AI assistant helps agents summarize tickets, draft replies, and reduce repetitive work. It improves speed and consistency while keeping humans in control."
    
    Context: {context}
    Key Points: {', '.join(key_points)}
    
    Output Format:
    {{
        "clean_summary": "",
        "main_message": "",
        "important_points": [],
        "missing_information": [],
        "possible_risks": []
    }}
    
    Rules:
    - Do not invent information.
    - Base your answer only on the provided input.
    - The summary should remove repetition, clarify vague inputs, and identify missing information.
    - Think through the input carefully, but return only a concise structured answer.
    - Return a clear summary in proper JSON format.
    """
    return call_json_llm([{"role": "user", "content": prompt}])
