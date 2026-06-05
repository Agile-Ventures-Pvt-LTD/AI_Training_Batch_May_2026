# get input for prompt
# def get_user_input(blog_topic:str, target_audience:str, product_or_service_context:str, key_points:list, desired_tone:str, blog_length:str, seo_keywords:list, call_to_action:str, industry:str, avoid_cliams:list, brand_guidelines:str):
def get_user_input():
    print("Please provide the following information for the blog post:")
    
    blog_topic = input(f"1. Blog Topic:".strip())
    
    target_audience = input(f"2. Target Audience:".strip())
   
    product_or_service_context = input(f"3. Product or Service Context:".strip())
    
    total_key_points = int(input(f"How many key points would you like to include? (Enter a number):".strip()))
    key_points = [input(f"4. Key Point {i+1}:".strip()) for i in range(total_key_points)]
   
    desired_tone = input(f"5. Desired Tone:".strip())
   
    blog_length = input(f"6. Blog Length:".strip())
    
    total_seo_keywords = int(input(f"How many SEO keywords would you like to include? (Enter a number):".strip()))
    seo_keywords = [input(f"7. SEO Keyword {i+1}:".strip()) for i in range(total_seo_keywords)]
    
    call_to_action = input(f"8. Call to Action:".strip())

    industry = input(f"9. Industry:".strip())
    
    total_avoid_claims = int(input(f"How many claims would you like to avoid? (Enter a number):".strip()))
    avoid_claims = [input(f"10. Avoid Claim {i+1}:".strip()) for i in range(total_avoid_claims)]
    
    brand_guidelines = input(f"11. Brand Guidelines:".strip())

    prompt_details=dict(blog_topic=blog_topic, target_audience=target_audience, product_or_service_context=product_or_service_context, key_points=key_points, desired_tone=desired_tone, blog_length=blog_length, seo_keywords=seo_keywords, call_to_action=call_to_action, industry=industry, avoid_claims=avoid_claims, brand_guidelines=brand_guidelines)
    
    return prompt_details

prompt_details = get_user_input()

# validate inputs for prompt
# def validate_inputs(blog_topic:str, target_audience:str, product_or_service_context:str, key_points:list, desired_tone:str, blog_length:str, seo_keywords:list, call_to_action:str, industry:str, avoid_cliams:list, brand_guidelines:str):
def validate_inputs(prompt_details:dict):
    blog_topic = prompt_details.get("blog_topic")
    target_audience = prompt_details.get("target_audience")
    product_or_service_context = prompt_details.get("product_or_service_context")
    key_points = prompt_details.get("key_points")
    desired_tone = prompt_details.get("desired_tone")
    blog_length = prompt_details.get("blog_length")
    seo_keywords = prompt_details.get("seo_keywords")
    call_to_action = prompt_details.get("call_to_action")
    industry = prompt_details.get("industry")
    avoid_claims = prompt_details.get("avoid_claims")
    brand_guidelines = prompt_details.get("brand_guidelines")

    if not blog_topic:
        raise ValueError("Blog topic is required.")
    if not target_audience:
        raise ValueError("Target audience is required.")
    if not product_or_service_context:
        raise ValueError("Product or service context is required.")
    if not key_points:
        raise ValueError("At least one key point is required.")
    if not desired_tone:
        raise ValueError("Desired tone is required.")
    if not blog_length:
        raise ValueError("Blog length is required.")
    if not seo_keywords:
        raise ValueError("At least one SEO keyword is required.")
    if not call_to_action:
        raise ValueError("Call to action is required.")
    if not industry:
        raise ValueError("Industry is required.")
    if not brand_guidelines:
        raise ValueError("Brand guidelines are required.")
    
    
validate_inputs(prompt_details)