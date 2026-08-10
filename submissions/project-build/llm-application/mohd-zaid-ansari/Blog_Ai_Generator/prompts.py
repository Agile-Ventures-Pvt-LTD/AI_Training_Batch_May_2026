def intent_prompt(user_data):

    return f"""
Role:
You are a B2B content strategist who can classify the intent of blog clearly.

Task:
Classify blog intent can use following categories for intent classification:
-THOUGHT_LEADERSHIP
-PRODUCT_EDUCATION
-SEO_INFORMATIONAL
-LEAD_GENERATION
-COMPARISON
-ANNOUNCEMENT
-HOW_TO_GUIDE

Input:
{user_data}

Rules:
- Use only provided information.
- Think carefully.
- Return concise reasoning summary.
- Return only JSON.

Output:

{{
 "blog_intent":"",
 "target_reader_maturity":"",
 "recommended_content_angle":"",
 "reasoning_summary":""
}}
"""

def input_summary_prompt(user_data):

    return f"""
Role:
You are a Business Analyst who can summarize the input of any blog so that everyonr can 
easily understant what type of blog user wants.

Task:
Summarize the whole input before blog generation in which you should not miss any important informations
which can lead to any misunderstanding of blog input.

Input:
{user_data}

Return only JSON.:

{{
 "clean_summary":"",
 "main_message":"",
 "important_points":[],
 "missing_information":[],
 "possible_risks":[]
}}
"""

def outline_prompt(
    user_data,
    summary
):

    return f"""
Role:
You are a Content Architect who can generate a structured blog outline before
generating the full blog for easy understanding.

Example:

Input:
Artificial Intelligence

Output:
{{
 "title":"Lets Talk about Artificiall Intelligence"
 "outline": [
{{
"section_heading": "",
"section_purpose": "",
"key_points_to_cover": []
}}
],
"cta_placement": "",
"estimated_word_count": 500
}}

Generate outline for:

{user_data}

Summary:
{summary}

Return JSON only.
"""

def blog_prompt(
    user_data,
    intent,
    summary,
    outline
):

    return f"""
Role:
You are a Senior SEO Blog Writer you had generated about more that hundereds of blog on
various topics.

Intent Analysis:
{intent}

Summary:
{summary}

Outline:
{outline}

Must Include:
1. SEO-friendly title
2. Introduction
3. Body sections with headings
4. Practical examples or business context
5. Conclusion
6. Call to action

Rules:

- Use the selected tone.
- Include the given SEO keywords naturally.
- Avoid exaggerated or unsupported claims.
- Do not invent statistics.
- Do not mention customer names unless provided.
- Do not claim certifications, case studies, awards, or guarantees unless 
explicitly provided.
- Keep the writing professional and business-ready.

Generate complete blog.
"""

def seo_prompt(blog):

    return f"""
Role:
SEO Specialist where you had generated many blogs on set of 
defined seo rules.

Example:

Input Blog:
Artificial Intelligence

Output:
{{
 "seo_title":"Why AI is needed"
 "meta_description": "",
 "primary_keyword": "",
 "secondary_keywords": [],
 "suggested_slug": "",
 "search_intent": ""
}}

Rules:
- SEO title should be concise.
- Meta description should be under 160 characters.
- Keywords should be used naturally.
- Slug should be lowercase and hyphen-separated.

Now generate SEO metadata for:

{blog}
"""

def linkedin_prompt(blog):

    return f"""
Role:
LinkedIn Post Specialist who had posted many post on linkedin for different blogs
which got many likes and reposts.

Task:
Your task is to genrate a linkedin post where the post must include:
- Hook
- Short explanation
- Business relevance
- Call to action
- 3 to 5 relevant hashtags

Example:

Blog:
CRM Blog

Output:

{{
"linkedin_post": "",
"hashtags": []
}}

Generate LinkedIn post for:

{blog}
"""

def review_prompt(blog):

    return f"""
Role:
Editorial Reviewer who had reviewd many blogs and articles and give almost
perfect analysis on many factors.

Task:
Your task is to review the blog generated on different parameters and
score the different parameters.


Review:

{blog}

SCORING GUIDELINES (1 to 5):

- Relevance
- Clarity
- Structure
- Tone Alignment
- SEO Usage
- Hallucination Risk
- CTA Effectiveness

Output:
{{
"scores": {{
    "relevance": 0,
    "clarity": 0,
    "structure": 0,
    "tone_alignment": 0,
    "seo_usage": 0,
    "hallucination_risk": 0,
    "cta_effectiveness": 0
}}
"strengths": [],
"improvement_areas": [],
"final_quality_summary": ""
}}



Return JSON only.
"""

def hallucination_prompt(blog):

    return f"""
Role:
Fact Checking Assistant who find hallucination in blog statements.

Example:

Claim:
We reduce costs by 80%

Result:
Unsupported Claim

Example:

Claim:
Software helps manage tickets

Result:
Safe Claim

Analyze:

{blog}

Return JSON only.
"""


