def format_response(response):
    """Format agent response for display"""
    if isinstance(response, dict):
        return "\n".join([f"{k}: {v}" for k, v in response.items()])
    return str(response)
