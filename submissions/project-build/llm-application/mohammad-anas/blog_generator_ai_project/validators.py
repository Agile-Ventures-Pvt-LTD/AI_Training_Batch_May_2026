def validate_inputs(data: dict) -> list:
    """Validates user inputs based on business rules. Returns a list of errors."""
    errors = []
    
    if not data.get("blog_topic"):
        errors.append("Blog topic cannot be empty.")
    if not data.get("target_audience"):
        errors.append("Target audience cannot be empty.")
    if len(data.get("key_points", [])) < 3:
        errors.append("Please provide at least 3 key points before generating the blog.")
    if not data.get("blog_length"):
        errors.append("Blog length must be specified.")
    if len(data.get("seo_keywords", [])) < 2:
        errors.append("Please provide at least 2 SEO keywords.")
    if not data.get("call_to_action"):
        errors.append("Call to action cannot be empty.")
        
    return errors