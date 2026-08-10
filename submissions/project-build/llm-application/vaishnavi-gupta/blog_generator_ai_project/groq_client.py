from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(
    api_key = "GROQ_API_KEY",
    
    )


def call_llm(prompt, blog_topic, target_audience, product_or_service_context, key_points, desired_tone,
             blog_length, seo_keywords, call_to_action, industry, avoid_claims, avoid_guidelines, temperature=0.3):
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            
                {"role":"user", "content":prompt},
                {"role": "assistant", "content":response}
        
        ],
        max_tokens=2000,
        temperature=temperature
    )

    return response.choices[0].message.content