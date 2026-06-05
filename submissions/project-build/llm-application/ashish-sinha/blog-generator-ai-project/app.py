import json
import os

from validators import validate_inputs
from groq_client import call_groq_model
from output_parser import parse_json
from prompt import *

# User Input

user_input = {
    "blog_topic": "How AI improves customer support",
    "target_audience": "Support leaders",
    "product_or_service_context": "AI Support Assistant",
    "key_points": [
        "Reduces repetitive work",
        "Summarizes tickets",
        "Suggests replies"
    ],
    "desired_tone": "Professional",
    "blog_length": "900 words",
    "seo_keywords": [
        "AI customer support",
        "support automation"
    ],
    "call_to_action": "Book a demo"
}

# Validation

validate_inputs(user_input)

print("Inputs validated")

# Intent Analysis

print("Generating intent analysis...")

intent = parse_json(
    call_groq_model(
        prompt_intent(user_input)
    )
)

# Summary

print("Generating summary...")

summary = parse_json(
    call_groq_model(
        prompt_summarize(user_input)
    )
)

# Outline


print("Generating outline...")

outline = parse_json(
    call_groq_model(
        prompt_outline(summary)
    )
)

# Blog


print("Generating blog...")

blog = call_groq_model(
    prompt_blog(
        summary,
        outline,
        user_input
    ),
    max_tokens=3000
)


# SEO Metadata

print("Generating SEO metadata...")

seo = parse_json(
    call_groq_model(
        prompt_seo(blog)
    )
)

# LinkedIn Post

print("Generating LinkedIn post...")

linkedin = parse_json(
    call_groq_model(
        prompt_linkedin(blog)
    )
)


# Quality Review

print("Generating quality review...")

quality = parse_json(
    call_groq_model(
        prompt_quality(blog)
    )
)

# Hallucination Check

print("Running hallucination check...")

try:
    hallucination = parse_json(
        call_groq_model(
            prompt_hallucination(blog),
            max_tokens=2500
        )
    )

except Exception as e:

    print(f"Hallucination check failed: {e}")

    hallucination = {
        "status": "failed",
        "error": str(e)
    }


# Final Output

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
        "model_used": os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        ),
        "temperature": 0.3,
        "total_steps_completed": 8
    }
}

# Debug Serialization Check

print("\nChecking JSON serializability...\n")

for key, value in final_output.items():
    try:
        json.dumps(value)
        print(f"✓ {key}")
    except TypeError as e:
        print(f"✗ {key}: {e}")

# Save Output

os.makedirs(
    "outputs",
    exist_ok=True
)

output_file = "outputs/blog_output.json"

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        final_output,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"\n Blog saved successfully: {output_file}")