import json
import os
import sys

from validators import validate_inputs
from groq_client import call_groq_model

from prompt import (
    zero,
    basic_rules,
    intent_prompt_template as INTENT_PROMPT,
    summary_prompt_template as SUMMARY_PROMPT,
    outline_prompt_template as OUTLINE_PROMPT,
    blog_prompt_template as BLOG_PROMPT,
    seo_linkedin_prompt_template as SEO_PROMPT,
    quality_review_prompt_template as QUALITY_PROMPT,
    hallucination_check_prompt_template as HALLUCINATION_PROMPT,
)

from output_parser import parse_json


sample_input = {
    "blog_topic": "How AI can improve customer support operations",
    "target_audience": "Customer support leaders",
    "product_or_service_context": "AI support assistant",
    "key_points": ["Reduces repetitive work", "Summarizes tickets", "Suggests replies"],
    "desired_tone": "Professional",
    "blog_length": "900 words",
    "seo_keywords": ["AI customer support", "support automation"],
    "call_to_action": "Book a demo",
}


errors = validate_inputs(sample_input)
if errors:
    print("Input validation failed:")
    for e in errors:
        print("-", e)
    sys.exit(1)

user_input = json.dumps(sample_input, indent=2)

intent = parse_json(
    call_groq_model(
        INTENT_PROMPT.format(zero=zero, context=user_input, basic_rules=basic_rules)
    )
)

summary = parse_json(
    call_groq_model(
        SUMMARY_PROMPT.format(zero=zero, context=user_input, basic_rules=basic_rules)
    )
)

outline = parse_json(
    call_groq_model(
        OUTLINE_PROMPT.format(zero=zero, context=user_input, intent_json=json.dumps(intent), basic_rules=basic_rules)
    )
)

blog_raw = call_groq_model(
    BLOG_PROMPT.format(zero=zero, context=user_input, summary_json=json.dumps(summary), outline_json=json.dumps(outline), basic_rules=basic_rules),
    max_tokens=3000,
)

try:
    blog = parse_json(blog_raw)
except Exception:
    blog = blog_raw

seo = parse_json(
    call_groq_model(
        SEO_PROMPT.format(zero=zero, context=user_input, blog_text=blog if isinstance(blog, str) else json.dumps(blog), basic_rules=basic_rules)
    )
)

linkedin = seo.get("linkedin_post") if isinstance(seo, dict) else {}

quality = parse_json(
    call_groq_model(
        QUALITY_PROMPT.format(zero=zero, context=user_input, blog_text=blog if isinstance(blog, str) else json.dumps(blog), basic_rules=basic_rules)
    )
)

hallucination = parse_json(
    call_groq_model(
        HALLUCINATION_PROMPT.format(zero=zero, context=user_input, blog_text=blog if isinstance(blog, str) else json.dumps(blog), basic_rules=basic_rules)
    )
)

final_output = {
    "blog_intent_analysis": intent,
    "input_summary": summary,
    "blog_outline": outline,
    "final_blog": blog,
    "seo_metadata": seo,
    "linkedin_post": linkedin,
    "quality_review": quality,
    "hallucination_check": hallucination,
    "generation_metadata": {
        "model_used": "llama-3.3-70b-versatile",
        "temperature": 0.3,
        "total_steps_completed": 8,
    },
}

os.makedirs("outputs", exist_ok=True)

with open("outputs/sample_blog_output.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=4, ensure_ascii=False)

print("Blog package generated successfully.")
