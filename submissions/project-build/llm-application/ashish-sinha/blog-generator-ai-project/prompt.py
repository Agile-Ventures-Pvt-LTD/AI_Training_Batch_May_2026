import json

def prompt_intent(user_input):

    return f"""
You are a B2B content strategist. You have to provide me prompt intent according to user input and classify the blog intent.

Task:
Classify the blog intent.

Possible Categories:
THOUGHT_LEADERSHIP
PRODUCT_EDUCATION
SEO_INFORMATIONAL
LEAD_GENERATION
COMPARISON
ANNOUNCEMENT
HOW_TO_GUIDE

Rules:
- Use only provided data
- Do not invent facts
- Return JSON only

Input:
{user_input}

Output:
{{
"blog_intent":"",
"target_reader_maturity":"",
"recommended_content_angle":"",
"reasoning_summary":""
}}
"""

def prompt_summarize(user_input):

    return f"""
You are a business analyst.

Summarize the input.

Identify:
1. Main message
2. Important points
3. Missing information
4. Risks

Return JSON only.

Input:
{user_input}
"""

def prompt_blog(
        summary,
        outline,
        user_input):

    return f"""
You are a Senior SEO Blog Writer.

Write a complete blog.

Rules:
- Use provided information only
- Do not invent statistics
- Do not invent awards
- Do not invent certifications
- Use SEO keywords naturally
- Include CTA

Summary:
{summary}

Outline:
{outline}

User Data:
{user_input}
"""
def prompt_outline(summary):

    return f"""
You are a content architect.

Example:

Input:
AI in sales

Output:
{{
"title":"How AI Improves Sales Productivity",
"outline":[
{{
"section_heading":"Why Sales Teams Struggle",
"section_purpose":"Pain points"
}}
]
}}

Now create outline.

Input:
{summary}

Return JSON only.
"""

def prompt_seo(blog):

    return f"""
Example

Input:
Blog about AI Support

Output:
{{
"seo_title":"AI Customer Support Guide",
"meta_description":"Learn how AI helps support teams.",
"primary_keyword":"AI customer support",
"secondary_keywords":["support automation"],
"suggested_slug":"ai-customer-support-guide",
"search_intent":"informational"
}}

Now process:

{blog}
"""

def prompt_linkedin(blog):

    return f"""
You are a LinkedIn content specialist.

Generate:

1 Hook
2 Summary
3 CTA
4 Hashtags

Return JSON.

Blog:
{blog}
"""
def prompt_quality(blog):

    return f"""
You are an editorial reviewer.

Score:

Relevance
Clarity
Structure
Tone Alignment
SEO Usage
Hallucination Risk
CTA Effectiveness

Return JSON.

Blog:
{blog}
"""

def prompt_hallucination(blog):

    return f"""
You are a fact-checking assistant.

Identify:

1 Claims requiring verification
2 Unsupported claims
3 Safe claims
4 Recommended edits

Return JSON.

Blog:
{blog}
"""
