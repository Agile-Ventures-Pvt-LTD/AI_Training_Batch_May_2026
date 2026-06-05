zero = "You are an AI assistant."

basic_rules = """Rules:
- Use only the provided input.
- Do not invent facts, statistics, awards, customer names, or unsupported claims.
- If information is missing, say it is not provided.
- Return valid JSON only.
"""

intent_prompt_template = """{zero}
Task: Classify the blog intent.
Input:
{context}

{basic_rules}

Output JSON:
{{
  "blog_intent": "",
  "target_reader_maturity": "",
  "recommended_content_angle": "",
  "reasoning_summary": ""
}}
"""

summary_prompt_template = """{zero}
Task: Summarize the user-provided blog requirements.
Input:
{context}

{basic_rules}

Output JSON:
{{
  "clean_summary": "",
  "main_message": "",
  "important_points": [],
  "missing_information": [],
  "possible_risks": []
}}
"""

outline_prompt_template = """{zero}
Task: Generate a structured blog outline.
Input:
{context}

Blog intent analysis:
{intent_json}

{basic_rules}

Output JSON:
{{
  "title": "",
  "outline": [
    {{
      "section_heading": "",
      "section_purpose": "",
      "key_points_to_cover": []
    }}
  ],
  "cta_placement": "",
  "estimated_word_count": 0
}}
"""

blog_prompt_template = """{zero}
Task: Write a complete blog draft.
Input:
{context}

Summary:
{summary_json}

Outline:
{outline_json}

{basic_rules}

Output JSON:
{{
  "final_blog": ""
}}
"""

seo_linkedin_prompt_template = """{zero}
Task: Generate SEO metadata and a LinkedIn post.

Example Input:
topic: AI customer support
seo_keywords: [AI customer support, support automation]
call_to_action: Book a demo

Example Output:
{{
  "seo_metadata": {{
    "seo_title": "AI Customer Support: Automate Smarter Service",
    "meta_description": "Discover how AI improves customer support productivity while keeping agents in control.",
    "primary_keyword": "AI customer support",
    "secondary_keywords": ["support automation", "customer service AI"],
    "suggested_slug": "ai-customer-support-support-automation",
    "search_intent": "informational"
  }},
  "linkedin_post": {{
    "linkedin_post": "",
    "hashtags": ["#AI", "#CustomerSupport", "#SupportAutomation"]
  }}
}}

Input:
{context}

Blog text:
{blog_text}

{basic_rules}

Output JSON:
{{
  "seo_metadata": {{
    "seo_title": "",
    "meta_description": "",
    "primary_keyword": "",
    "secondary_keywords": [],
    "suggested_slug": "",
    "search_intent": ""
  }},
  "linkedin_post": {{
    "linkedin_post": "",
    "hashtags": []
  }}
}}
"""

quality_review_prompt_template = """{zero}
Task: Review the blog draft for quality.
Input:
{context}

Blog text:
{blog_text}

{basic_rules}

Output JSON:
{{
  "scores": {{
    "relevance": 0,
    "clarity": 0,
    "structure": 0,
    "tone_alignment": 0,
    "seo_usage": 0,
    "hallucination_risk": 0,
    "cta_effectiveness": 0
  }},
  "strengths": [],
  "improvement_areas": [],
  "final_quality_summary": ""
}}
"""

hallucination_check_prompt_template = """{zero}
Task: Check the blog for hallucination risk.
Input:
{context}

Blog text:
{blog_text}

{basic_rules}

Output JSON:
{{
  "claims_requiring_verification": [],
  "unsupported_claims": [],
  "safe_claims": [],
  "recommended_edits": []
}}
"""
