from groq_client import call_llm


def generate_draft(outline: str, validated_inputs: dict) -> str:
    prompt = f"""
    Role: You are a senior SEO blog writer for a B2B marketing team.
    Task: Draft a complete, business-ready blog using only the provided inputs.
    
    Outline: {outline}
    Blog Topic: {validated_inputs['blog_topic']}
    Target Audience: {validated_inputs['target_audience']}
    Product / Service Context: {validated_inputs['product_or_service_context']}
    Key Points: {', '.join(validated_inputs['key_points'])}
    Tone: {validated_inputs['desired_tone']}
    Length: {validated_inputs['blog_length']}
    SEO Keywords: {', '.join(validated_inputs['seo_keywords'])}
    Call to Action: {validated_inputs['call_to_action']}
    Industry: {validated_inputs.get('industry', '')}
    Avoided Claims: {', '.join(validated_inputs.get('avoid_claims', []))}
    Guidelines: {validated_inputs.get('brand_guidelines', '')}
    
    Rules:
    - Include an SEO-friendly title.
    - Include an introduction, clear body sections with headings, practical business context, conclusion, and CTA.
    - Use the SEO keywords naturally.
    - Avoid hype.
    - Respect brand guidelines.
    - Do not invent facts, statistics, customer names, awards, certifications, financial results, legal claims, guarantees, or case studies.
    - If information is missing, write around it without pretending it was provided.
    - Keep the writing professional and ready for human editorial review.
    """
    return call_llm([{"role": "user", "content": prompt}])
