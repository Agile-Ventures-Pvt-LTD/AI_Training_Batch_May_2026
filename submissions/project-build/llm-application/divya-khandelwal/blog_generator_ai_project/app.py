from groq_client import call_groq_model
from validators import validate_groq_api_key, validate_blog_request
import os
import json
from dotenv import load_dotenv
from prompts import system_message, user_message
from output_parser import parse_groq_response, store_response_in_json
load_dotenv()

def main():

    api_key = os.environ["GROQ_API_KEY"]
    try:
        validate_groq_api_key(api_key)
    except ValueError as e:
        print(f"API Key validation error: {e}")
        return
    
    
    blog_request = {
        "blog_topic": "The Future of AI in Content Marketing",
        "target_audience": "Marketing professionals",
        "product_or_service_context": "AI-powered content creation tools",
        "key_points_to_cover": "Benefits, implementation strategies, and future trends",
        "desired_tone": "Professional and informative",
        "blog_length": "Medium, around 900 words",
        "seo_keywords": ["AI customer support", "support automation", "customer service AI"],
        "call_to_action": "Book a demo to explore how AI can improve your support operations.",
        "industry": "SaaS",
        "avoid_claims": [
            "Do not claim guaranteed cost reduction.",
            "Do not claim full automation of customer support.",
            "Do not mention any customer case study."
        ],
        "brand_guidelines": "Use clear business language. Avoid hype. Keep the tone trustworthy and practical."
    }
    
    try:
        validate_blog_request(blog_request)
    except ValueError as e:
        print(f"Blog request validation error: {e}")
        return 
    
    
    response = call_groq_model(system_message, user_message)
    
   
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True) 
    output_file_path = os.path.join(output_folder, "sample_blog_output.json")
    
    store_response_in_json(response, output_file_path)
    
    print(f"GROQ Model Response has been saved to {output_file_path}")

if __name__ == "__main__":
    main()
