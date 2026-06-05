import os
import json
import time
from validators import validate_inputs
from groq_client import call_groq_model, MODEL_NAME
from output_parser import parse_json_safely
import prompts

def main():
    print("Starting AI Blog Generator Pipeline...")
    start_time = time.time()

    # 1. Sample Input
    user_input = {
        "blog_topic": "How AI can improve customer support operations",
        "target_audience": "Customer support leaders, CX heads, and operations managers",
        "product_or_service_context": "An AI-powered customer support assistant.",
        "key_points": [
            "Support teams are facing increasing ticket volumes.",
            "Agents spend a lot of time reading long customer conversations.",
            "AI can summarize tickets and suggest draft replies."
        ],
        "desired_tone": "Professional, practical, and business-oriented",
        "blog_length": "Medium, around 900 words",
        "seo_keywords": ["AI customer support", "support automation", "customer service AI"],
        "call_to_action": "Book a demo to explore how AI can improve your support operations.",
        "industry": "SaaS",
        "avoid_claims": ["Do not claim guaranteed cost reduction."],
        "brand_guidelines": "Use clear business language. Avoid hype."
    }

    # 2. Validation
    errors = validate_inputs(user_input)
    if errors:
        print("[ERROR] Validation Failed:")
        for e in errors: print(f"- {e}")
        return

    payload_str = prompts.build_user_prompt(user_input)

    # 3. Intent Classification
    print("Step 1/7: Classifying Intent...")
    intent_raw = call_groq_model(payload_str, prompts.INTENT_SYSTEM_PROMPT, temperature=0.0)
    intent_json = parse_json_safely(intent_raw)

    # 4. Summarization
    print("Step 2/7: Summarizing Inputs...")
    summary_raw = call_groq_model(payload_str, prompts.SUMMARY_SYSTEM_PROMPT, temperature=0.1)
    summary_json = parse_json_safely(summary_raw)

    # 5. Outline
    print("Step 3/7: Generating Outline...")
    outline_context = f"Summary: {json.dumps(summary_json)}\nUser Rules: {payload_str}"
    outline_raw = call_groq_model(outline_context, prompts.OUTLINE_SYSTEM_PROMPT, temperature=0.3)
    outline_json = parse_json_safely(outline_raw)

    # 6. Blog Generation
    print("Step 4/7: Writing Blog Draft...")
    blog_context = f"Outline: {json.dumps(outline_json)}\nTone: {user_input['desired_tone']}"
    final_blog = call_groq_model(blog_context, prompts.BLOG_WRITER_SYSTEM_PROMPT, temperature=0.6, max_tokens=3000)

    # 7. SEO & LinkedIn (Combined)
    print("Step 5/7: Generating SEO & Social...")
    seo_raw = call_groq_model(final_blog, prompts.SEO_SOCIAL_SYSTEM_PROMPT, temperature=0.2)
    seo_json = parse_json_safely(seo_raw)

    # 8. Quality Review
    print("Step 6/7: Quality Review...")
    quality_raw = call_groq_model(final_blog, prompts.QUALITY_REVIEW_SYSTEM_PROMPT, temperature=0.0)
    quality_json = parse_json_safely(quality_raw)

    # 9. Hallucination Check
    print("Step 7/7: Hallucination Check...")
    hallucination_raw = call_groq_model(final_blog, prompts.HALLUCINATION_SYSTEM_PROMPT, temperature=0.0)
    hallucination_json = parse_json_safely(hallucination_raw)

    # 10. Compile Final Output
    final_package = {
        "blog_intent_analysis": intent_json,
        "input_summary": summary_json,
        "blog_outline": outline_json,
        "final_blog": final_blog,
        "seo_metadata": {k: v for k, v in seo_json.items() if k != "linkedin_post" and k != "hashtags"},
        "linkedin_post": {"linkedin_post": seo_json.get("linkedin_post"), "hashtags": seo_json.get("hashtags")},
        "quality_review": quality_json,
        "hallucination_check": hallucination_json,
        "generation_metadata": {
            "model_used": MODEL_NAME,
            "temperature": 0.3,
            "total_steps_completed": 7,
            "execution_time_seconds": round(time.time() - start_time, 2)
        }
    }

    # Save Output
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/sample_blog_output.json", "w") as f:
        json.dump(final_package, f, indent=4)
        
    print(f"\n✅ Pipeline Complete in {final_package['generation_metadata']['execution_time_seconds']} seconds!")
    print("Output saved to: outputs/sample_blog_output.json")

if __name__ == "__main__":
    main()