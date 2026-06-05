from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

from prompts import system_message, user_message

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

def call_groq_model(system_message: str, user_message: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message.format(
                blog_topic="The Future of AI in Content Marketing",
                target_audience="Marketing professionals",
                product_or_service_context="AI-powered content creation tools",
                key_points_to_cover="Benefits, implementation strategies, and future trends",
                desired_tone="Professional and informative",
                blog_length="Medium, around 900 words",
                seo_keywords='["AI customer support", "support automation", "customer service AI"]',
                call_to_action="Book a demo to explore how AI can improve your support operations.",
                industry="SaaS",
                avoid_claims='["Do not claim guaranteed cost reduction.", "Do not claim full automation of customer support.", "Do not mention any customer case study."]',
                brand_guidelines="Use clear business language. Avoid hype. Keep the tone trustworthy and practical."
                
            )}
        ],
        temperature=0.2,
        max_tokens=2000
    )
    return response.choices[0].message.content

