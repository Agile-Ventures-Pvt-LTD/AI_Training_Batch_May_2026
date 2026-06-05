import os
import sys
import json
from dotenv import load_dotenv
import groq
from validators import validate_input
from groq_client import call_groq_model
from output_parser import parse_json
from prompts import (INTENT_PROMPT, SUMMARY_PROMPT,OUTLINE_PROMPT,BLOG_PROMPT,SEO_PROMPT,LINKEDIN_PROMPT,QUALITY_PROMPT,HALLUCINATION_PROMPT)

def generate_blog(data):
    validate_input(data)
    user_input = json.dumps(data,indent=2)
    print("Intent Classification")
    intent = parse_json(
        call_groq_model(
            INTENT_PROMPT.format(
                user_input=user_input
            )
        )
    )
    print("Input Summary")

    summary = parse_json(
        call_groq_model(
            SUMMARY_PROMPT.format(
                user_input=user_input
            )
        )
    )

    print("Outline Generation")

    outline = parse_json(
        call_groq_model(
            OUTLINE_PROMPT.format(
                summary=json.dumps(summary)
            )
        )
    )

    print("Blog Generation")

    blog = call_groq_model(
        BLOG_PROMPT.format(
            context=user_input
        ),
        max_tokens=4000
    )

    print("SEO Metadata")

    seo = parse_json(
        call_groq_model(
            SEO_PROMPT.format(
                blog=blog
            )
        )
    )

    print("LinkedIn Post")

    linkedin = parse_json(
        call_groq_model(
            LINKEDIN_PROMPT.format(
                blog=blog
            )
        )
    )

    print("quality_review")

    quality = parse_json(
        call_groq_model(
            QUALITY_PROMPT.format(
                blog=blog
            )
        )
    )

    print("hallucination_check")

    hallucination = parse_json(
        call_groq_model(
            HALLUCINATION_PROMPT.format(
                blog=blog
            )
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
            "temperature": 0.7,
            "total_steps_completed": 8
        }
    }

    os.makedirs(
        "outputs",
        exist_ok=True
    )

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

    return final_output


if __name__ == "__main__":

    sample_input = {
        "blog_topic":
            "How AI can improve customer support operations",

        "target_audience":
            "Customer support leaders and CX heads",

        "product_or_service_context":
            "AI-powered support assistant",

        "key_points": [
            "Reduces repetitive ticket handling",
            "Summarizes customer issues",
            "Suggests replies to support agents",
            "Improves response time",
            "Does not replace humans"
        ],

        "desired_tone":
            "Professional",

        "blog_length":
            "900 words",

        "seo_keywords": [
            "AI customer support",
            "support automation",
            "customer service AI"
        ],

        "call_to_action":
            "Book a product demo"
    }

    try:
        result = generate_blog(
            sample_input
        )

    except groq.RateLimitError as exc:
        print("Groq API rate limit reached:", exc)
        print("Please wait and try again later, or switch to a different model/account.")
        sys.exit(1)

    except Exception as exc:
        print("Error generating blog:", exc)
        sys.exit(1)

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )