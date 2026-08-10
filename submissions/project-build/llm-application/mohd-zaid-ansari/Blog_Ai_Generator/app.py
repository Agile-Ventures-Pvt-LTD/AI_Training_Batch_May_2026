from validators import validate_input
from groq_client import call_groq_model
from prompts import *
from output_parser import parse_json
from output_builder import build_final_output
from save_output import save_output

def collect_user_input():

    return {

        "blog_topic": input("Blog Topic: "),

        "target_audience": input(
            "Target Audience: "
        ),

        "product_or_service_context": input(
            "Product/Service Context: "
        ),

        "key_points": [
            x.strip()
            for x in input(
                "Key Points (comma separated): "
            ).split(",")
        ],

        "desired_tone": input(
            "Desired Tone: "
        ),

        "blog_length": input(
            "Blog Length: "
        ),

        "seo_keywords": [
            x.strip()
            for x in input(
                "SEO Keywords (comma separated): "
            ).split(",")
        ],

        "call_to_action": input(
            "Call To Action: "
        ),

        "industry": input(
            "Industry (optional): "
        ),

        "avoid_claims": [
            x.strip()
            for x in input(
                "Avoid Claims (comma separated): "
            ).split(",")
        ],

        "brand_guidelines": input(
            "Brand Guidelines: "
        )
    }

user_data=collect_user_input()

errors = validate_input(user_data)

if errors:
    print(errors)
    raise Exception("Validation Failed")

intent_analysis = parse_json(
    call_groq_model(
        intent_prompt(user_data)
    )
)

input_summary = parse_json(
    call_groq_model(
        input_summary_prompt(user_data)
    )
)

blog_outline = parse_json(
    call_groq_model(
        outline_prompt(
            user_data,
            input_summary
        )
    )
)

final_blog = call_groq_model(
    blog_prompt(
        user_data,
        intent_analysis,
        input_summary,
        blog_outline
    )
)

seo_metadata = parse_json(
    call_groq_model(
        seo_prompt(final_blog)
    )
)

linkedin_post = parse_json(
    call_groq_model(
        linkedin_prompt(final_blog)
    )
)

quality_review = parse_json(
    call_groq_model(
        review_prompt(final_blog)
    )
)

hallucination_check = parse_json(
    call_groq_model(
        hallucination_prompt(final_blog)
    )
)

final_output = build_final_output(
    intent_analysis,
    input_summary,
    blog_outline,
    final_blog,
    seo_metadata,
    linkedin_post,
    quality_review,
    hallucination_check
)

