def intent_prompt(blog):

    return f"""
You are a Senior Content Strategist.

Analyze the blog request and classify the content intent.

Allowed Intent Categories:
- THOUGHT_LEADERSHIP
- PRODUCT_EDUCATION
- SEO_INFORMATIONAL
- LEAD_GENERATION
- COMPARISON
- ANNOUNCEMENT
- HOW_TO_GUIDE

Blog Topic:
{blog["blog_topic"]}

Target Audience:
{blog["target_audience"]}

Product / Service Context:
{blog["product_or_service_context"]}

Key Points:
{blog["key_points"]}

Return ONLY valid JSON.

{{
  "blog_intent":"",
  "target_reader_maturity":"",
  "recommended_content_angle":"",
  "reasoning_summary":""
}}
"""


def outline_prompt(blog, summary, intent):

    return f"""
You are a Senior Blog Strategist.

Create a complete blog outline.

Blog Topic:
{blog["blog_topic"]}

Target Audience:
{blog["target_audience"]}

Intent Analysis:
{intent}

Summary:
{summary}

Desired Length:
{blog["blog_length"]}

Requirements:
- Generate an SEO-friendly title.
- Create introduction direction.
- Create 4-6 sections.
- Provide section purpose.
- Suggest conclusion.
- Suggest CTA placement.

Return ONLY valid JSON.

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

def blog_generation_prompt(blog, summary, outline, intent):

    return f"""
You are a Senior B2B Blog Writer.

Write a complete business-ready blog.

Requirements:
- Follow the provided outline.
- Use the selected tone.
- Include SEO keywords naturally.
- Do NOT invent statistics.
- Do NOT invent customer stories.
- Do NOT claim certifications.
- Do NOT claim awards.
- Do NOT claim guarantees.
- Do NOT use external facts.
- Use only information provided.

Blog Topic:
{blog["blog_topic"]}

Target Audience:
{blog["target_audience"]}

Product Context:
{blog["product_or_service_context"]}

Intent:
{intent}

Summary:
{summary}

Outline:
{outline}

Tone:
{blog["desired_tone"]}

SEO Keywords:
{blog["seo_keywords"]}

Call To Action:
{blog["call_to_action"]}

Return ONLY valid JSON.

{{
  "blog_title":"",
  "blog_content":""
}}
"""


def seo_prompt(blog, generated_blog):

    return f"""
You are an SEO Specialist.

Generate SEO metadata.

Requirements:
- SEO title should be concise.
- Meta description under 160 characters.
- Use keywords naturally.
- Slug must be lowercase and hyphen-separated.

SEO Keywords:
{blog["seo_keywords"]}

Blog:
{generated_blog}

Return ONLY valid JSON.

{{
  "seo_title":"",
  "meta_description":"",
  "primary_keyword":"",
  "secondary_keywords":[],
  "suggested_slug":"",
  "search_intent":""
}}
"""


def linkedin_prompt(blog, generated_blog):

    return f"""
You are a LinkedIn Content Marketing Expert.

Create a LinkedIn post promoting the blog.

Requirements:
- Strong opening hook.
- Short explanation.
- Business relevance.
- Clear CTA.
- 3 to 5 hashtags.

Blog:
{generated_blog}

Return ONLY valid JSON.

{{
  "linkedin_post":"",
  "hashtags":[]
}}
"""



def review_prompt(generated_blog, blog):

    return f"""
You are a Senior Content Quality Reviewer.

Evaluate the blog.

Scoring Range:
1 = Poor
5 = Excellent

Hallucination Risk:
1 = Very Low Risk
5 = Very High Risk

Original Request:
{blog}

Generated Blog:
{generated_blog}

Return ONLY valid JSON.

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


def hallucination_prompt(generated_blog):

    return f"""
You are an AI Fact Verification Assistant.

Review the blog and identify statements requiring verification.

Flag:
- Numerical claims
- Market leadership claims
- Guaranteed outcomes
- Legal claims
- Compliance claims
- Customer success claims
- Competitor comparisons
- Certifications
- Awards

Blog:
{generated_blog}

Return ONLY valid JSON.

{{
  "claims_requiring_verification":[],
  "unsupported_claims":[],
  "safe_claims":[],
  "recommended_edits":[]
}}
"""




def summary_prompt(blog):

    return f"""
You are a Content Planning Assistant.

Summarize the user's input.

Requirements:
- Remove repetition.
- Clarify vague ideas.
- Preserve business goals.
- Identify missing information.
- Identify potential content risks.

Blog Topic:
{blog["blog_topic"]}

Product Context:
{blog["product_or_service_context"]}

Key Points:
{blog["key_points"]}

Return ONLY valid JSON.

{{
  "clean_summary":"",
  "main_message":"",
  "important_points":[],
  "missing_information":[],
  "possible_risks":[]
}}
"""