
from groq_client import call_groq
from output_parser import safe_json_parse
from prompts import (
    BLOG_INTENT_PROMPT,
    INPUT_SUMMARIZATION_PROMPT,
    BLOG_OUTLINE_PROMPT,
    BLOG_DRAFT_PROMPT,
    SEO_METADATA_PROMPT,
    LINKEDIN_POST_PROMPT,
    QUALITY_REVIEW_PROMPT,
    HALLUCINATION_CHECK_PROMPT,
)
from validators import BlogRequest
from config import GROQ_MODEL

def generate_blog_package(user_input: BlogRequest):
    # Blog intent classification
    blog_intent_response = call_groq(
        [
            {"role": "user", "content": BLOG_INTENT_PROMPT.format(user_input=user_input)},
        ],
        temperature=0.3,
        max_tokens=200,
    )
    blog_intent = safe_json_parse(blog_intent_response)

    # Input summarization
    input_summarization_response = call_groq(
        [
            {"role": "user", "content": INPUT_SUMMARIZATION_PROMPT.format(user_input=user_input)},
        ],
        temperature=0.3,
        max_tokens=200,
    )
    input_summarization = safe_json_parse(input_summarization_response)

    # Blog outline generation
    blog_outline_response = call_groq(
        [
            {"role": "user", "content": BLOG_OUTLINE_PROMPT.format(user_input=user_input)},
        ],
        temperature=0.3,
        max_tokens=200,
    )
    blog_outline = safe_json_parse(blog_outline_response)

    # Blog draft generation
    blog_draft_response = call_groq(
        [
            {"role": "user", "content": BLOG_DRAFT_PROMPT.format(user_input=user_input, blog_outline=blog_outline)},
        ],
        temperature=0.3,
        max_tokens=2000,
    )
    blog_draft = blog_draft_response

    # SEO metadata generation
    seo_metadata_response = call_groq(
        [
            {"role": "user", "content": SEO_METADATA_PROMPT.format(user_input=user_input)},
        ],
        temperature=0.3,
        max_tokens=200,
    )
    seo_metadata = safe_json_parse(seo_metadata_response)

    # LinkedIn post generation
    linkedin_post_response = call_groq(
        [
            {"role": "user", "content": LINKEDIN_POST_PROMPT.format(user_input=user_input)},
        ],
        temperature=0.3,
        max_tokens=200,
    )
    linkedin_post = linkedin_post_response

    # Quality review
    quality_review_response = call_groq(
        [
            {"role": "user", "content": QUALITY_REVIEW_PROMPT.format(blog_draft=blog_draft)},
        ],
        temperature=0.3,
        max_tokens=200,
    )
    quality_review = safe_json_parse(quality_review_response)

    # Hallucination check
    hallucination_check_response = call_groq(
        [
            {"role": "user", "content": HALLUCINATION_CHECK_PROMPT.format(blog_draft=blog_draft)},
        ],
        temperature=0.3,
        max_tokens=200,
    )
    hallucination_check = safe_json_parse(hallucination_check_response)

    # Final output package
    final_output = {
        "blog_intent_analysis": blog_intent,
        "input_summary": input_summarization,
        "blog_outline": blog_outline,
        "final_blog": blog_draft,
        "seo_metadata": seo_metadata,
        "linkedin_post": linkedin_post,
        "quality_review": quality_review,
        "hallucination_check": hallucination_check,
        "generation_metadata": {
            "model_used": GROQ_MODEL,
            "temperature": 0.3,
            "total_steps_completed": 8,
        },
    }

    return final_output

if __name__ == "__main__":
    user_input = BlogRequest(
        blog_topic="How AI can improve customer support operations",
        target_audience="Customer support leaders, CX heads, and operations managers",
        product_or_service_context="An AI-powered customer support assistant that helps agents summarize tickets, draft responses, identify escalation risks, and reduce repetitive manual work.",
        key_points=[
            "Support teams are facing increasing ticket volumes.",
            "Agents spend a lot of time reading long customer conversations.",
            "AI can summarize tickets and suggest draft replies.",
            "AI should assist human agents, not replace them.",
            "The solution can help improve consistency and response speed.",
            "Sensitive customer data must be handled carefully.",
        ],
        desired_tone="Professional, practical, and business-oriented",
        blog_length="Medium, around 900 words",
        seo_keywords=["AI customer support", "support automation", "customer service AI"],
        call_to_action="Book a demo to explore how AI can improve your support operations.",
    )

    final_output = generate_blog_package(user_input)
    print(final_output)