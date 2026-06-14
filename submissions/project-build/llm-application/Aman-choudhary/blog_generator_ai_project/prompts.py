INTENT_PROMPT = """
You are a B2B Content Strategist.
Analyze the blog request.
Input:{user_input}
{{
  "blog_intent":"",
  "target_reader_maturity":"",
  "recommended_content_angle":"",
  "reasoning_summary":""
}}
"""
SUMMARY_PROMPT = """
You are a Business Analyst.
Summarize the input.
Input:{user_input}
{{
  "clean_summary":"",
  "main_message":"",
  "important_points":[],
  "missing_information":[],
  "possible_risks":[]
}}
"""
OUTLINE_PROMPT = """
You are a Content Architect.
Generate a blog outline
Input:
{summary}
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
  "estimated_word_count":0
}}
"""
BLOG_PROMPT = """
You are a Senior SEO Blog Writer.
Write a complete blog.
Rules:
1 Use only provided information.
2 Do not invent facts.
3 Do not invent statistics.
3 Do not invent customer stories.
4 Use SEO keywords naturally.
5 Follow the requested tone.
Input:{context}
"""
SEO_PROMPT = """
Generate SEO metadata.{{
  "seo_title":"",
  "meta_description":"",
  "primary_keyword":"",
  "secondary_keywords":[],
  "suggested_slug":"",
  "search_intent":""
}}
Blog:{blog}
"""
LINKEDIN_PROMPT = """
Generate a LinkedIn post.
{{
  "linkedin_post":"",
  "hashtags":[]
}}
Blog:
{blog}
"""
QUALITY_PROMPT = """
You are an Editorial Reviewer.
Review the blog
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
Blog:{blog}
"""
HALLUCINATION_PROMPT = """
You are a Fact Checking Assistant.
{{
  "claims_requiring_verification":[],
  "unsupported_claims":[],
  "safe_claims":[],
  "recommended_edits":[]
}}
Blog:{blog}
"""