def validate_groq_api_key(api_key):
    if not api_key.startswith("gsk_"):
        raise ValueError("Invalid GROQ API key format. It should start with 'gsk_'.")
    if len(api_key) < 20:
        raise ValueError("Invalid GROQ API key length. It should be at least 20 characters long.")
    
def validate_blog_request(blog_request):
    required_fields = [
        "blog_topic",
        "target_audience",
        "product_or_service_context",
        "key_points_to_cover",
        "desired_tone",
        "blog_length",
        "seo_keywords",
        "call_to_action",
        "industry",
        "avoid_claims",
        "brand_guidelines"
    ]
    
    missing_fields = [field for field in required_fields if field not in blog_request]
    if missing_fields:
        raise ValueError(f"Missing required fields in blog request: {', '.join(missing_fields)}")
    
    if not isinstance(blog_request["seo_keywords"], list):
        raise ValueError("The 'seo_keywords' field should be a list of strings.")
    
    if not isinstance(blog_request["avoid_claims"], list):
        raise ValueError("The 'avoid_claims' field should be a list of strings.")
    
    if not isinstance(blog_request["brand_guidelines"], str):
        raise ValueError("The 'brand_guidelines' field should be a string.")
    


