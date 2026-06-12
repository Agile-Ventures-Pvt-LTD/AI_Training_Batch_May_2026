import json


def blog_intent_prompt(
    user_input: dict
):

    return f"""
Role:
You are a senior B2B content strategist.

Task:
Classify blog intent.

Input:
{json.dumps(user_input, indent=2)}

Rules:
- Use only provided information.
- Do not invent facts.
- Think carefully.
- Return concise reasoning summary.
- Return valid JSON only.

Output:
{{
 "blog_intent":"",
 "target_reader_maturity":"",
 "recommended_content_angle":"",
 "reasoning_summary":""
}}
"""


def summarization_prompt(
    user_input: dict
):

    return f"""
Role:
You are a business analyst.

Task:
Summarize the user notes.

Input:
{json.dumps(user_input, indent=2)}

Rules:
- Remove repetition.
- Identify missing information.
- Mention risks.
- Return JSON only.

Output:
{{
 "clean_summary":"",
 "main_message":"",
 "important_points":[],
 "missing_information":[],
 "possible_risks":[]
}}
"""


def outline_prompt(
    summary: dict,
    intent: dict
):

    return f"""
Role:
You are a content architect.

Task:
Create blog outline.

Summary:
{json.dumps(summary, indent=2)}

Intent:
{json.dumps(intent, indent=2)}

Return JSON only.

Output:
{{
 "title":"",
 "outline":[
   {{
      "section_heading":"",
      "section_purpose":"",
      "key_points_to_cover":[]
   }}
 ],
 "cta_placement":"",
 "estimated_word_count":900
}}
"""


def blog_generation_prompt(
    user_input,
    summary,
    outline
):

    return f"""
Role:
You are a senior SEO blog writer.

Task:
Generate complete blog.

User Input:
{json.dumps(user_input, indent=2)}

Summary:
{json.dumps(summary, indent=2)}

Outline:
{json.dumps(outline, indent=2)}

Rules:
- Use provided keywords naturally.
- No fake statistics.
- No unsupported claims.
- No customer names.
- No awards or certifications.
- No external facts.
- Professional tone.

Generate complete blog only.
"""


def seo_prompt(
    blog_text
):

    return f"""
Role:
You are an SEO specialist.

Example:

Input:
Blog about AI Support

Output:
{{
 "seo_title":"AI Support Guide",
 "meta_description":"Learn how AI improves support operations.",
 "primary_keyword":"AI support",
 "secondary_keywords":["automation"],
 "suggested_slug":"ai-support-guide",
 "search_intent":"informational"
}}

Actual Blog:
{blog_text}

Return JSON only.
"""


def linkedin_prompt(
    blog_text
):

    return f"""
Role:
You are a LinkedIn content marketer.

Example:

Output:
{{
 "linkedin_post":"...",
 "hashtags":["#AI"]
}}

Blog:
{blog_text}

Return JSON only.
"""


def quality_review_prompt(
    blog_text
):

    return f"""
Role:
You are an editorial reviewer.

Review this blog:

{blog_text}

Return JSON:

{{
 "scores": {{
   "relevance":0,
   "clarity":0,
   "structure":0,
   "tone_alignment":0,
   "seo_usage":0,
   "hallucination_risk":0,
   "cta_effectiveness":0
 }},
 "strengths":[],
 "improvement_areas":[],
 "final_quality_summary":""
}}
"""


def hallucination_prompt(
    blog_text
):

    return f"""
Role:
You are a fact-checking assistant.

Blog:

{blog_text}

Rules:
- Flag unsupported claims.
- Flag numerical claims.
- Flag market leadership claims.
- Flag customer success claims.

Return JSON:

{{
 "claims_requiring_verification":[],
 "unsupported_claims":[],
 "safe_claims":[],
 "recommended_edits":[]
}}
"""