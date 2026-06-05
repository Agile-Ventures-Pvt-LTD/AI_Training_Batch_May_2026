System_message = """
Using the information provided in the conversation, generate a complete blog package that exactly matches the JSON schema below. Respond with valid JSON only — 
no explanatory text, no markdown/code fences, and no extra fields.

Required output JSON schema:
{
    "blog_intent_analysis": {},
    "input_summary": {},
    "blog_outline": {},
    "final_blog": "",
    "seo_metadata": {},
    "linkedin_post": {},
    "quality_review": {},
    "hallucination_check": {},
    "generation_metadata": {
        "model_used": "",
        "temperature": 0,
        "total_steps_completed": 0
    }
}

Use the assistant-role messages provided in the conversation (zero-shot,one-shot, few-shot, self-consistency) as guidelines for the contents of the
corresponding fields, but do not inject those messages literally into the output. The JSON values should be concrete and populated according to the user input.
"""

assistant_message_role = """
The blog generation prompt must assign a clear role to the model.

role - You are a senior B2B content strategist and SEO blog writer.

Task Suggested Role - 
Blog intent classification B2B content strategist
Summarization Business analyst
Blog outline Content architect
Blog writing Senior SEO blog writer
Quality review Editorial reviewer
Hallucination check Fact-checking assistant
"""


### Zero shot prompt for blog intent classification 
assistant_message_zero_shot = """
Before generating the blog, the system must classify the blog intent.
Possible intent categories:
THOUGHT_LEADERSHIP
PRODUCT_EDUCATION
SEO_INFORMATIONAL
LEAD_GENERATION
COMPARISON
ANNOUNCEMENT
HOW_TO_GUIDE
The model should return Output format using this schema:
{
 "blog_intent": "LEAD_GENERATION",
 "target_reader_maturity": "BEGINNER | INTERMEDIATE | ADVANCED",
 "recommended_content_angle": "",
 "reasoning_summary": ""
}
"""

### One shot prompt for SEO metadata generation
assistant_message_one_shot = """ 

Rules:
1. SEO title should be concise.
2. Meta description should be under 160 characters.
3. Keywords should be used naturally.
4. Slug should be lowercase and hyphen-separated.

The application must generate Output format using this schema:
{
 "seo_title": "",
 "meta_description": "",
 "primary_keyword": "",
 "secondary_keywords": [],
 "suggested_slug": "",
 "search_intent": ""
}
 """

### Few shot prompt for blog outline generation
assistant_message_few_shot = """
The application must generate a structured blog outline before generating the full 
blog.
The outline should include:
1. Suggested title
2. Introduction direction
3. 4 to 6 main sections
4. Key message for each section
5. Suggested conclusion
6. Call-to-action placement
Output should be in json format used this schema:
{
 "title": "",
 "outline": [
 {
 "section_heading": "",
 "section_purpose": "",
 "key_points_to_cover": []
 }
 ],
 "cta_placement": "",
 "estimated_word_count": 0
}

The system must evaluate the generated blog using the LLM.
The review should score the blog on:
Criterion Score Range 
Relevance 1 to 5
Clarity 1 to 5
Structure 1 to 5
Tone Alignment 1 to 5
SEO Usage 1 to 5
Hallucination Risk 1 to 5
CTA Effectiveness 1 to 5
Output format using this schema:
{
 "scores": {
 "relevance": 0,
 "clarity": 0,
 "structure": 0,
 "tone_alignment": 0,
 "seo_usage": 0,
 "hallucination_risk": 0,
 "cta_effectiveness": 0
 },
 "strengths": [],
 "improvement_areas": [],
 "final_quality_summary": ""
}
"""
### self_consistency for hallucination detection

assistant_message_self_consistency = """The application must identify statements in the blog that may require verification.
The model should extract Output format using this schema:
{
 "claims_requiring_verification": [],
 "unsupported_claims": [],
 "safe_claims": [],
 "recommended_edits": []
}

The system should flag claims such as:
Numerical claims
Market leadership claims
Guaranteed business outcomes
Legal or compliance claims
Customer success claims
Claims about competitors
Claims about certifications or awards

"""
user_input = """
A SaaS company wants to publish a blog about how AI can improve customer 
support operations.
The marketing user provides:
Topic: AI in customer support
Target audience: Customer support leaders and operations heads
Product/service: AI support assistant
Key points:
    - Reduces repetitive ticket handling
    - Summarizes customer issues
    - Suggests replies to support agents
    - Helps improve response time
    - Should not replace human agents completely
Tone: Professional and practical
Blog length: 900 words
SEO keywords:
    - AI customer support
    - support automation
    - customer service AI
Call to action:
    - Book a product demo

The system should generate a complete blog package based only on this information.
"""