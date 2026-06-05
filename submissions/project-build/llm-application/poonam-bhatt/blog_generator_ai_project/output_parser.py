from groq_client import parse_json_safe, call_groq

from prompts import (intent_prompt,summary_prompt,outline_prompt,
                     blog_generation_prompt,seo_prompt,
                     linkedin_prompt,review_prompt,hallucination_prompt,)

def run_pipeline(blog):

    results = {}

    # FR-3
    intent = parse_json_safe(
        call_groq(intent_prompt(blog))
    )

    results["blog_intent_analysis"] = intent

    # FR-4
    summary = parse_json_safe(
        call_groq(summary_prompt(blog))
    )

    results["input_summary"] = summary

    # FR-5
    outline = parse_json_safe(
        call_groq(
            outline_prompt(
                blog,
                summary,
                intent
            )
        )
    )

    results["blog_outline"] = outline

    # FR-6
    generated_blog = parse_json_safe(
        call_groq(
            blog_generation_prompt(
                blog,
                summary,
                outline,
                intent
            )
        )
    )

    results["final_blog"] = generated_blog

    # FR-7
    seo_metadata = parse_json_safe(
        call_groq(
            seo_prompt(
                blog,
                generated_blog
            )
        )
    )

    results["seo_metadata"] = seo_metadata

    # FR-8
    linkedin_post = parse_json_safe(
        call_groq(
            linkedin_prompt(
                blog,
                generated_blog
            )
        )
    )

    results["linkedin_post"] = linkedin_post

    # FR-9
    quality_review = parse_json_safe(
        call_groq(
            review_prompt(
                generated_blog,
                blog
            )
        )
    )

    results["quality_review"] = quality_review

    # FR-10
    hallucination_check = parse_json_safe(
        call_groq(
            hallucination_prompt(
                generated_blog
            )
        )
    )

    results["hallucination_check"] = hallucination_check

    # FR-11
    results["generation_metadata"] = {
        "model_used": "llama-3.1-70b-versatile",
        "temperature": 0,
        "total_steps_completed": 8
    }

    return results