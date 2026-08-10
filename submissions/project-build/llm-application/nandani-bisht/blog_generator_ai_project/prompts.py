def intent_classification_prompt(user_data):
    return f"""
Role: You are a senior B2B content strategist.
Task: Classify the blog intent based on the following user inputs.
Instructions: Return only JSON matching this schema exactly:
{{
  "blog_intent": "",
  "target_reader_maturity": "",
  "recommended_content_angle": "",
  "reasoning_summary": ""
}}
Allowed intents: THOUGHT_LEADERSHIP, PRODUCT_EDUCATION, SEO_INFORMATIONAL, LEAD_GENERATION, COMPARISON, ANNOUNCEMENT, HOW_TO_GUIDE
Target reader maturity must be one of: BEGINNER, INTERMEDIATE, ADVANCED
Input:
{user_data}
Note: Provide a concise reasoning summary explaining why this intent fits the input.
"""


def summarization_prompt(user_data):
    return f"""
Role: You are a business analyst.
Task: Summarize the user-provided inputs into a clean summary.
Instructions: Return only JSON matching this schema exactly:
{{
  "clean_summary": "",
  "main_message": "",
  "important_points": [],
  "missing_information": [],
  "possible_risks": []
}}
Input:
{user_data}
Note: The summary should remove repetition, clarify vague inputs, and identify missing information.
"""


def outline_prompt(user_data):
    # Few-shot examples
    example = '''
Example
Input: {"blog_topic":"How to reduce cloud costs","key_points":["rightsizing","reserved instances","monitoring"]}
Output:
{
  "title": "Practical Ways to Reduce Cloud Costs",
  "outline": [
    {"section_heading":"Introduction",
    "section_purpose":"Set the scene",
    "key_points_to_cover":["cost trends","why it matters"]},
    
    {"section_heading":"Rightsizing instances",
    "section_purpose":"Explain rightsizing",
    "key_points_to_cover":["identify idle resources","tools to help"]}
  ],
  "cta_placement":"End",
  "estimated_word_count":900
}
'''
    return f"""
Role: You are a content architect.
Task: Generate a structured blog outline (title, 4-6 main sections) based on input.
Few-shot example:
{example}
Input:
{user_data}
Return only JSON matching this schema:
{{
 "title":"",
 "outline":[
   {{"section_heading":"","section_purpose":"","key_points_to_cover":[]}}
 ],
 "cta_placement":"",
 "estimated_word_count":0
}}
Note: Create 4-6 sections. Each section should include a clear purpose and 2-4 key points.
"""


def blog_prompt(user_data):
    return f"""
Role: You are a senior SEO blog writer.
Task: Write a full blog draft based on the following inputs and outline.
Input:
{user_data}
Instructions:
- Use the provided tone and include the SEO keywords naturally.
- Do NOT invent any facts, statistics, customer names, awards, or guarantees unless provided.
- If information is missing, state what is missing briefly in a JSON field and proceed.
Return JSON only:
{{
  "seo_title":"",
  "blog":"",
  "notes":""  
}}
Note: Include a concise reasoning summary (one sentence) at the top of your response but return only the JSON fields.
"""


def seo_prompt(user_data):
    # One-shot example
    example = '''
Example Input: {"title":"Reduce Cloud Costs Fast","primary_keyword":"cloud cost reduction","secondary_keywords":["rightsizing","reserved instances"]}
Example Output:
{
  "seo_title":"Reduce Cloud Costs: Practical Steps for 2026",
  "meta_description":"Learn practical steps to reduce cloud costs with rightsizing and reserved instances. (Under 160 chars)",
  "primary_keyword":"cloud cost reduction",
  "secondary_keywords":["rightsizing","reserved instances"],
  "suggested_slug":"reduce-cloud-costs-practical-steps",
  "search_intent":"Informational"
}
'''
    return f"""

Role: You are an SEO specialist.
One-shot example:
{example}
Input:
{user_data}
Task: Return SEO metadata JSON only with keys: seo_title, meta_description, primary_keyword, secondary_keywords, suggested_slug, search_intent.
Rules: meta_description should be under 160 charact, slug lowercase hyphen-separated
"""


def linkedin_prompt(user_data):
    example = '''
Example Input: {"title":"Reduce Cloud Costs","summary":"Practical steps to reduce cloud bills."}
Example Output:
{
  "linkedin_post":"Hook. Short explanation. Business relevance. CTA.",
  "hashtags":["#cloud","#costs","#SaaS"]
}
'''
    return f"""
Role: You are a social media copywriter.
One-shot example:
{example}
Input:
{user_data}
Task: Produce JSON only: {{"linkedin_post":"","hashtags":[]}}. Include 3-5 relevant hashtags.
"""


def quality_review_prompt(user_data):
    # Few-shot examples
    example = '''
Example Input: {"blog":"A short blog about X"}
Example Output:
{
 "scores": {"relevance":4,"clarity":4,"structure":3,"tone_alignment":4,"seo_usage":3,"hallucination_risk":1,"cta_effectiveness":3},
 "strengths":["Clear intro"],
 "improvement_areas":["Add examples"],
 "final_quality_summary":"Good draft; needs examples and minor edits."
}
'''
    return f"""
Role: You are an editorial reviewer.
Few-shot example:
{example}
Input:
{user_data}
Task: Score the blog on a 1-5 scale for each criterion and return JSON with scores, strengths, improvement_areas, final_quality_summary. For hallucination_risk higher means riskier.
"""


def hallucination_prompt(user_data):
    return f"""
Role: You are a fact-checking assistant pro.
Task: Identify claims in the blog that may require verification.
Input:
{user_data}
Return JSON only:
{{
 "claims_requiring_verification": [],
 "unsupported_claims": [],
 "safe_claims": [],
 "recommended_edits": []
}}
Rules: Flag numerical claims, market leadership claims, guarantees, legal/compliance, customer names, certifications, and competitor comparisons.
"""