"""
Main application workflow.

Pipeline:

Step 1: Accept user inputs
Step 2: Validate inputs
Step 3: Classify blog intent
Step 4: Summarize input
Step 5: Generate outline
Step 6: Generate blog
Step 7: Generate SEO metadata
Step 8: Generate LinkedIn post
Step 9: Quality review
Step 10: Hallucination check
Step 11: Create final output package
Step 12: Save output
"""

from groq_client import call_groq_model

from validators import validate_inputs

from output_parser import (
    parse_json_response,
    save_output
)

from config import (
    INTENT_MAX_TOKENS,
    SUMMARY_MAX_TOKENS,
    OUTLINE_MAX_TOKENS,
    BLOG_MAX_TOKENS,
    SEO_MAX_TOKENS,
    LINKEDIN_MAX_TOKENS,
    QUALITY_MAX_TOKENS,
    HALLUCINATION_MAX_TOKENS,
    GROQ_MODEL
)

from prompts import (
    INTENT_SYSTEM_PROMPT,
    INTENT_USER_PROMPT,

    SUMMARY_SYSTEM_PROMPT,
    SUMMARY_USER_PROMPT,

    OUTLINE_SYSTEM_PROMPT,
    OUTLINE_USER_PROMPT,

    FULL_BLOG_SYSTEM_PROMPT,
    FULL_BLOG_USER_PROMPT,

    SEO_SYSTEM_PROMPT,
    SEO_USER_PROMPT,

    LINKEDIN_SYSTEM_PROMPT,
    LINKEDIN_USER_PROMPT,

    QUALITY_REVIEW_SYSTEM_PROMPT,
    QUALITY_REVIEW_USER_PROMPT,

    HALLUCINATION_SYSTEM_PROMPT,
    HALLUCINATION_USER_PROMPT
)


# ==========================================================
# STEP 1 - USER INPUT
# ==========================================================

def get_user_input():

    print("\nPlease provide the following information for the blog post:\n")

    blog_topic = input("1. Blog Topic: ")

    target_audience = input("2. Target Audience: ")

    product_or_service_context = input("3. Product or Service Context: ")

    total_key_points = int(input("How many key points would you like to include?: "))

    key_points = [
        input(f"4. Key Point {i+1}: ")
        for i in range(total_key_points)
    ]

    desired_tone = input("5. Desired Tone: ")

    blog_length = input("6. Blog Length: ")

    total_seo_keywords = int(
        input("How many SEO keywords would you like to include?: "))

    seo_keywords = [
        input(f"7. SEO Keyword {i+1}: ")
        for i in range(total_seo_keywords)
    ]

    call_to_action = input("8. Call to Action: ")

    industry = input("9. Industry: ")

    total_avoid_claims = int(input("How many claims would you like to avoid?: "))

    avoid_claims = [
        input(f"10. Avoid Claim {i+1}: ")
        for i in range(total_avoid_claims)
    ]

    brand_guidelines = input("11. Brand Guidelines: ")

    return {
        "blog_topic": blog_topic,
        "target_audience": target_audience,
        "product_or_service_context": product_or_service_context,
        "key_points": key_points,
        "desired_tone": desired_tone,
        "blog_length": blog_length,
        "seo_keywords": seo_keywords,
        "call_to_action": call_to_action,
        "industry": industry,
        "avoid_claims": avoid_claims,
        "brand_guidelines": brand_guidelines
    }


# ==========================================================
# MAIN PIPELINE
# ==========================================================

def main():

    try:

        # Step 1
        prompt_details = get_user_input()

        # Step 2
        validate_inputs(prompt_details)

        print("\nGenerating blog package...\n")

        # ==================================================
        # Step 3 - Intent Analysis
        # ==================================================

        intent_response = call_groq_model(
            system_prompt=INTENT_SYSTEM_PROMPT,
            user_prompt=INTENT_USER_PROMPT.format(
                prompt_details=prompt_details
            ),
            max_tokens=INTENT_MAX_TOKENS
        )
        
        print("\nintent Response:")
        print(intent_response)

        blog_intent_analysis = parse_json_response(intent_response)

        # ==================================================
        # Step 4 - Input Summary
        # ==================================================

        summary_response = call_groq_model(
            system_prompt=SUMMARY_SYSTEM_PROMPT,
            user_prompt=SUMMARY_USER_PROMPT.format(
                prompt_details=prompt_details
            ),
            max_tokens=SUMMARY_MAX_TOKENS
        )
        print("\nSummary Response:")
        print(summary_response)

        input_summary = parse_json_response(summary_response)

        # ==================================================
        # Step 5 - Blog Outline
        # ==================================================

        outline_response = call_groq_model(
            system_prompt=OUTLINE_SYSTEM_PROMPT,
            user_prompt=OUTLINE_USER_PROMPT.format(
                prompt_details=prompt_details
            ),
            max_tokens=OUTLINE_MAX_TOKENS
        )
        print("\nOutline Response:")
        print(outline_response)
        blog_outline = parse_json_response(outline_response)

        # ==================================================
        # Step 6 - Full Blog
        # ==================================================

        blog_response = call_groq_model(
            system_prompt=FULL_BLOG_SYSTEM_PROMPT,
            user_prompt=FULL_BLOG_USER_PROMPT.format(
                user_input=prompt_details,
                input_summary=input_summary,
                blog_outline=blog_outline
            ),
            max_tokens=BLOG_MAX_TOKENS
        )

        print("\nFull Blog Response:")
        print(blog_response)

        # final_blog = parse_json_response(blog_response)
        # blog_content = final_blog["final_blog"]
        blog_content = blog_response

        # ==================================================
        # Step 7 - SEO Metadata
        # ==================================================

        seo_response = call_groq_model(
            system_prompt=SEO_SYSTEM_PROMPT,
            user_prompt=SEO_USER_PROMPT.format(
                blog_content=blog_content
            ),
            max_tokens=SEO_MAX_TOKENS
        )
        print("\nSEO Metadata Response:")
        print(seo_response)

        seo_metadata = parse_json_response(seo_response)

        # ==================================================
        # Step 8 - LinkedIn Post
        # ==================================================

        linkedin_response = call_groq_model(
            system_prompt=LINKEDIN_SYSTEM_PROMPT,
            user_prompt=LINKEDIN_USER_PROMPT.format(
                blog_content=blog_content
            ),
            max_tokens=LINKEDIN_MAX_TOKENS
        )
        print("\nLinkedIn Post Response:")
        print(linkedin_response)

        linkedin_post = parse_json_response(linkedin_response)

        # ==================================================
        # Step 9 - Quality Review
        # ==================================================

        quality_response = call_groq_model(
            system_prompt=QUALITY_REVIEW_SYSTEM_PROMPT,
            user_prompt=QUALITY_REVIEW_USER_PROMPT.format(
                blog_content=blog_content
            ),
            max_tokens=QUALITY_MAX_TOKENS
        )
        print("\nQuality Review Response:")
        print(quality_response)
        quality_review = parse_json_response(quality_response)

        # ==================================================
        # Step 10 - Hallucination Check
        # ==================================================

        hallucination_response = call_groq_model(
            system_prompt=HALLUCINATION_SYSTEM_PROMPT,
            user_prompt=HALLUCINATION_USER_PROMPT.format(
                blog_content=blog_content
            ),
            max_tokens=HALLUCINATION_MAX_TOKENS
        )
        print("\nHallucination Check Response:")
        print(hallucination_response)

        hallucination_check = parse_json_response(hallucination_response)

        # ==================================================
        # Step 11 - Final Output Package
        # ==================================================

        final_output = {
            "blog_intent_analysis":
                blog_intent_analysis,

            "input_summary":
                input_summary,

            "blog_outline":
                blog_outline,

            "final_blog":
                blog_content,

            "seo_metadata":
                seo_metadata,

            "linkedin_post":
                linkedin_post,

            "quality_review":
                quality_review,

            "hallucination_check":
                hallucination_check,

            "generation_metadata": {
                "model_used": GROQ_MODEL,
                "temperature": 0.2,
                "total_steps_completed": 8
            }
        }

        # ==================================================
        # Step 12 - Save Output
        # ==================================================

        file_path = save_output(final_output)

        print("\nBlog generated successfully.")
        print(f"\nOutput saved to: {file_path}")

    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()