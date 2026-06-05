import json

from validators import validate_inputs
from groq_client import call_groq_model

from prompts import (
    INTENT_PROMPT,
    SUMMARY_PROMPT,
    OUTLINE_PROMPT,
    BLOG_PROMPT,
    SEO_PROMPT,
    LINKEDIN_PROMPT,
    QUALITY_PROMPT,
    HALLUCINATION_PROMPT
)

from output_parser import parse_json


sample_input = {
    "blog_topic":
        "How AI can improve customer support operations",

    "target_audience":
        "Customer support leaders",

    "product_or_service_context":
        "AI support assistant",

    "key_points": [
        "Reduces repetitive work",
        "Summarizes tickets",
        "Suggests replies"
    ],

    "desired_tone":
        "Professional",

    "blog_length":
        "900 words",

    "seo_keywords": [
        "AI customer support",
        "support automation"
    ],

    "call_to_action":
        "Book a demo"
}


validate_inputs(sample_input)

user_input = json.dumps(
    sample_input,
    indent=2
)

intent = parse_json(
    call_groq_model(
        INTENT_PROMPT.format(
            user_input=user_input
        )
    )
)

summary = parse_json(
    call_groq_model(
        SUMMARY_PROMPT.format(
            user_input=user_input
        )
    )
)

outline = parse_json(
    call_groq_model(
        OUTLINE_PROMPT.format(
            summary=json.dumps(summary)
        )
    )
)

blog = call_groq_model(
    BLOG_PROMPT.format(
        summary=json.dumps(summary),
        outline=json.dumps(outline)
    ),
    max_tokens=3000
)

seo = parse_json(
    call_groq_model(
        SEO_PROMPT.format(blog=blog)
    )
)

linkedin = parse_json(
    call_groq_model(
        LINKEDIN_PROMPT.format(blog=blog)
    )
)

quality = parse_json(
    call_groq_model(
        QUALITY_PROMPT.format(blog=blog)
    )
)

hallucination = parse_json(
    call_groq_model(
        HALLUCINATION_PROMPT.format(blog=blog)
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
        "model_used":
            "llama-3.3-70b-versatile",
        "temperature": 0.3,
        "total_steps_completed": 8
    }
}

with open(
    "outputs/sample_blog_output.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        final_output,
        f,
        indent=4,
        ensure_ascii=False
    )

print(
    "Blog package generated successfully."
)