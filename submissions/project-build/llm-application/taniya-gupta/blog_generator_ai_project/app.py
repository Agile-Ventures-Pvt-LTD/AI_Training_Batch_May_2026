import json
import os
from groq_client import call_groq_model
from prompts import (intent_classification_prompt,summary_prompt, outline_generation_prompt, blog_post_generation_prompt, quality_review_prompt, seo_linkedin_prompt, hallucination_control_prompt,)
from output_parser import parse_json, build_final_package
from validators import validate_blog_input
import config


def build_prompt_context(user_input, summary=None, outline=None, blog_text=None):
    return {
        "blog_topic": user_input.get("blog_topic", ""),
        "target_audience": user_input.get("target_audience", ""),
        "product_or_service_context": user_input.get("product_or_service_context", ""),
        "key_points": ", ".join(user_input.get("key_points", [])),
        "key_points_json": json.dumps(user_input.get("key_points", []),),
        "desired_tone": user_input.get("desired_tone", ""),
        "blog_length": user_input.get("blog_length", ""),
        "seo_keywords": ", ".join(user_input.get("seo_keywords", [])),
        "call_to_action": user_input.get("call_to_action", ""),
        "industry": user_input.get("industry", ""),
        "avoid_claims": ", ".join(user_input.get("avoid_claims", [])),
        "brand_guidelines": user_input.get("brand_guidelines", ""),
        "clean_summary": summary.get("clean_summary", "") if summary else "",
        "important_points_json": json.dumps(summary.get("important_points", []),) if summary else "[]",
        "outline_title": outline.get("title", "") if outline else "",
        "outline_json": json.dumps(outline) if outline else "{}",
        "estimated_word_count": outline.get("estimated_word_count", 0) if outline else 0,
        "blog_text": blog_text if blog_text else "",
    }


def generate_blog(user_input):
   
    validation_result = validate_blog_input(user_input)
    if not validation_result["valid"]:
        return {"error": "Validation failed"}
    
    results = {}
    steps_completed = 0
    
    # Blog intent classification
    prompt = intent_classification_prompt.format(**build_prompt_context(user_input))
    response = call_groq_model(prompt, temperature=0.3, max_tokens=config.DEFAULT_MAX_TOKENS)
    results["blog_intent_analysis"] = parse_json(response)
    steps_completed += 1
    print("Blog intent classification completed")
    
    # Input summarization
    prompt = summary_prompt.format(**build_prompt_context(user_input))
    response = call_groq_model(prompt, temperature=0.3, max_tokens=config.SUMMARY_MAX_TOKENS)
    summary = parse_json(response)
    results["input_summary"] = summary
    steps_completed += 1
    print("Input summary completed")
    
    # Blog outline generation
    prompt = outline_generation_prompt.format(**build_prompt_context(user_input, summary=summary))
    response = call_groq_model(prompt, temperature=0.3, max_tokens=config.OUTLINE_MAX_TOKENS)
    outline = parse_json(response)
    results["blog_outline"] = outline
    steps_completed += 1
    print("Blog outline generated")
    
    # Full blog generation
    prompt = blog_post_generation_prompt.format(**build_prompt_context(user_input, summary=summary, outline=outline))
    response = call_groq_model(prompt, temperature=0.3, max_tokens=config.BLOG_MAX_TOKENS)
    blog_data = parse_json(response)
    results["final_blog"] = blog_data.get("final_blog", "")
    blog_text = blog_data.get("final_blog", "")
    steps_completed += 1
    print(" Blog draft generated")
    
    # SEO metadata and LinkedIn post
    prompt = seo_linkedin_prompt.format(**build_prompt_context(user_input, outline=outline))
    response = call_groq_model(prompt, temperature=0.3, max_tokens=config.SEO_LINKEDIN_MAX_TOKENS)
    seo_linkedin_data = parse_json(response)
    results["seo_metadata"] = seo_linkedin_data.get("seo_metadata", {})
    results["linkedin_post"] = seo_linkedin_data.get("linkedin_post", {})
    steps_completed += 1
    
    # Quality review
    prompt = quality_review_prompt.format(**build_prompt_context(user_input, blog_text=blog_text))
    response = call_groq_model(prompt, temperature=0.3, max_tokens=config.QUALITY_REVIEW_MAX_TOKENS)
    results["quality_review"] = parse_json(response)
    steps_completed += 1
    
    # Hallucination checklist
    prompt = hallucination_control_prompt.format(blog_text=blog_text)
    response = call_groq_model(prompt, temperature=0.3, max_tokens=config.HALLUCINATION_CHECK_MAX_TOKENS)
    results["hallucination_check"] = parse_json(response)
    steps_completed += 1
    
    # Final
    results["generation_metadata"] = {
        "model_used": config.GROQ_MODEL,
        "temperature": 0.3,
        "total_steps_completed": steps_completed,
    }
    
    final_package = build_final_package(**results)
    
    # Save output
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(config.OUTPUT_DIR, "blog_output.json")
    with open(output_file, "w") as f:
        json.dump(final_package, f, indent=2)
    print(f" Output is saved")
    
    return final_package


def display_output(output):
    
    print("\n Blog is generated\n")

    print(" BLOG INTENT ANALYSIS:")
    intent = output.get("blog_intent_analysis", {})
    print(f"  Intent: {intent.get('blog_intent', 'N/A')}")
    print(f"  Reader Maturity: {intent.get('target_reader_maturity', 'N/A')}")
    print(f"  Content Angle: {intent.get('recommended_content_angle', 'N/A')}")
    
    print("\n INPUT SUMMARY:")
    summary = output.get("input_summary", {})
    print(f"  {summary.get('clean_summary', 'N/A')}")
    
    print("\n BLOG OUTLINE:")
    outline = output.get("blog_outline", {})
    print(f"  Title: {outline.get('title', 'N/A')}")
    print(f"  Sections: {len(outline.get('outline', []))}")
    print(f"  Est. Word Count: {outline.get('estimated_word_count', 'N/A')}")
    
    print("\n FINAL BLOG:")
    blog = output.get("final_blog", "")
    if blog:
        print(f"  {blog[:300]}...")
    
    print("\n SEO METADATA:")
    seo = output.get("seo_metadata", {})
    print(f"  Title: {seo.get('seo_title', 'N/A')}")
    print(f"  Meta: {seo.get('meta_description', 'N/A')}")
    
    print("\n LINKEDIN POST:")
    linkedin = output.get("linkedin_post", {})
    print(f"  {linkedin.get('linkedin_post', 'N/A')[:200]}...")
    
    print("\n QUALITY REVIEW:")
    quality = output.get("quality_review", {})
    scores = quality.get("scores", {})
    print(f"  Relevance: {scores.get('relevance', 'N/A')}/5")
    print(f"  Clarity: {scores.get('clarity', 'N/A')}/5")
    print(f"  Hallucination Risk: {scores.get('hallucination_risk', 'N/A')}/5 (higher = more risk)")
    
    print("\n HALLUCINATION CHECK:")
    hc = output.get("hallucination_check", {})
    print(f"  Claims to Verify: {len(hc.get('claims_requiring_verification', []))}")
    print(f"  Unsupported Claims: {len(hc.get('unsupported_claims', []))}")
    
    print("\n GENERATION METADATA:")
    meta = output.get("generation_metadata", {})
    print(f"  Model: {meta.get('model_used', 'N/A')}")
    print(f"  Steps Completed: {meta.get('total_steps_completed', 'N/A')}")
    

if __name__ == "__main__":
    sample_input = {
        "blog_topic": "How AI can improve customer support operations",
        "target_audience": "Customer support leaders, CX heads, and operations managers",
        "product_or_service_context": "An AI-powered customer support assistant that helps agents summarize tickets, draft responses, identify escalation risks, and reduce repetitive manual work.",
        "key_points": [
            "Support teams are facing increasing ticket volumes.",
            "Agents spend a lot of time reading long customer conversations.",
            "AI can summarize tickets and suggest draft replies.",
            "AI should assist human agents, not replace them.",
            "The solution can help improve consistency and response speed.",
            "Sensitive customer data must be handled carefully."
        ],
        "desired_tone": "Professional, practical, and business-oriented",
        "blog_length": "Medium, around 900 words",
        "seo_keywords": [
            "AI customer support",
            "support automation",
            "customer service AI"
        ],
        "call_to_action": "Book a demo to explore how AI can improve your support operations.",
        "industry": "SaaS",
        "avoid_claims": [
            "Do not claim guaranteed cost reduction.",
            "Do not claim full automation of customer support.",
            "Do not mention any customer case study."
        ],
        "brand_guidelines": "Use clear business language. Avoid hype. Keep the tone trustworthy and practical."
    }
    
    output = generate_blog(sample_input)
    display_output(output)