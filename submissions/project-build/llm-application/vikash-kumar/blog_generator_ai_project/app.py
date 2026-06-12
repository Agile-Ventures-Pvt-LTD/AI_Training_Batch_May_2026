from groq_client import groq_client

from validators import (
    validate_blog_input
)

from output_parser import (
    extract_json,
    save_output
)

from prompts import (
    blog_intent_prompt,
    summarization_prompt,
    outline_prompt,
    blog_generation_prompt,
    seo_prompt,
    linkedin_prompt,
    quality_review_prompt,
    hallucination_prompt
)


TEST_INPUT = {
    "blog_topic":
    "How AI can improve customer support operations",

    "target_audience":
    "Customer support leaders, CX heads, and operations managers",

    "product_or_service_context":
    "AI-powered support assistant",

    "key_points": [
        "Support teams face rising ticket volumes",
        "AI summarizes tickets",
        "AI suggests replies",
        "AI assists humans",
        "Improves response speed"
    ],

    "desired_tone":
    "Professional",

    "blog_length":
    "medium",

    "seo_keywords": [
        "AI customer support",
        "support automation",
        "customer service AI"
    ],

    "call_to_action":
    "Book a demo"
}


def run_pipeline():

    errors = validate_blog_input(
        TEST_INPUT
    )

    if errors:
        print(errors)
        return

    print("Step 1: Intent")

    intent = extract_json(
        groq_client.generate(
            blog_intent_prompt(
                TEST_INPUT
            )
        )
    )

    print("Step 2: Summary")

    summary = extract_json(
        groq_client.generate(
            summarization_prompt(
                TEST_INPUT
            )
        )
    )

    print("Step 3: Outline")

    outline = extract_json(
        groq_client.generate(
            outline_prompt(
                summary,
                intent
            )
        )
    )

    print("Step 4: Blog")

    blog = groq_client.generate(
        blog_generation_prompt(
            TEST_INPUT,
            summary,
            outline
        ),
        max_tokens=2500
    )

    print("Step 5: SEO")

    seo = extract_json(
        groq_client.generate(
            seo_prompt(blog)
        )
    )

    print("Step 6: LinkedIn")

    linkedin = extract_json(
        groq_client.generate(
            linkedin_prompt(blog)
        )
    )

    print("Step 7: Quality")

    quality = extract_json(
        groq_client.generate(
            quality_review_prompt(blog)
        )
    )

    print("Step 8: Hallucination")

    hallucination = extract_json(
        groq_client.generate(
            hallucination_prompt(blog)
        )
    )

    final_output = {
        "blog_intent_analysis":
        intent,

        "input_summary":
        summary,

        "blog_outline":
        outline,

        "final_blog":
        blog,

        "seo_metadata":
        seo,

        "linkedin_post":
        linkedin,

        "quality_review":
        quality,

        "hallucination_check":
        hallucination,

        "generation_metadata": {
            "model_used":
            "llama-3.3-70b-versatile",

            "temperature":
            0.3,

            "total_steps_completed":
            8
        }
    }

    save_output(
        final_output
    )

    print(
        "Blog package generated successfully."
    )


if __name__ == "__main__":
    run_pipeline()